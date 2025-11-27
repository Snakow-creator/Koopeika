from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import desc, select

from secret.config import POSTGRES_DATABASE, POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT
from operations.verification import checker_id
from database.models import Transaction, User, Payment, async_session, AsyncAttrs
from database.errors_config import ManyTransactionsError, BigCommentError
from loggers.logs import log

import asyncpg


async def connect():
    # подключение к базе данных
    conn = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DATABASE,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
    return conn


class SelectUser:
    def __init__(self, tg_id: int, user: User):
        self.id = tg_id
        self.user = user

    @classmethod
    async def load(cls, tg_id):
        conn = await connect()
        user = await conn.fetchrow("SELECT * FROM users WHERE tg_id = $1", tg_id)
        if not user:
            await conn.execute(
                """
                INSERT INTO users
                (tg_id, full_balance, time_zone, value, style, registered, premium_until)
                VALUES
                ($1, $2, $3, $4, $5, $6, $7)
            """,
                tg_id,
                0,
                "+3",
                "USD",
                "symbols",
                datetime.now(timezone.utc),
                datetime.now(timezone.utc),
            )
            log.debug(f"Add user {tg_id}")
            await conn.close()
            return await cls.load(tg_id)
        return cls(tg_id, user)

    async def premium(self):
        if self.user["premium_until"] > datetime.utcnow():
            return "premium"
        return False


class Transactions(SelectUser):
    def __init__(self, tg_id, user: User, transactions: Transaction):
        self.id = tg_id
        self.user = user
        self.transactions = transactions

    @classmethod
    async def load(cls, tg_id):
        conn = await connect()
        user = await conn.fetchrow("SELECT * FROM users WHERE tg_id = $1", tg_id)
        transactions = await conn.fetch(
            """
                SELECT *
                FROM transactions
                WHERE user_id = $1
                AND closed = False
                ORDER BY time DESC
            """,
            tg_id,
        )
        log.debug("get user and transaction db data")
        await conn.close()
        return cls(tg_id, user, transactions)

    async def add(self, value, assets, description):
        conn = await connect()
        if len(description) >= 30:
            raise BigCommentError()
        # если транзакции больше 50 - выдаем ошибку
        max_trs = 50
        if self.user["premium_until"] > datetime.utcnow():
            max_trs = 300

        if len(list(self.transactions)) == max_trs:
            raise ManyTransactionsError()

        time = datetime.now(ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d %H:%M")

        await conn.execute(
            """
            INSERT INTO transactions
            (value, user_id, amount, time, description)
            VALUES
            ($1, $2, $3, $4, $5)
        """,
            value,
            self.user["tg_id"],
            assets,
            time,
            description,
        )
        log.debug(f"Add transaction {self.user['tg_id']}")
        await conn.close()

    async def edit(self, value: float, num_id: int):
        # check exists user taransaction
        op = await checker_id(num_id, self.transactions)
        conn = await connect()
        await conn.fetchrow(
            """
            UPDATE transactions
            SET amount = $1
            WHERE id = $2
            """,
            op + str(value),
            num_id,
        )
        log.debug(f"Edit transaction {num_id}")
        await conn.close()

    async def delete(self, num_id: int, tg_id: int):
        # check exists user taransaction
        await checker_id(num_id, self.transactions)
        conn = await connect()
        await conn.execute(
        """
            UPDATE transactions
            SET closed = True
            WHERE id = $1
        """,
            num_id)
        log.debug(f"Delete transaction {num_id}")
        await conn.close()


class Payments(SelectUser):
    def __init__(self, tg_id: int, user: User, payments: Payment):
        self.user_id = tg_id
        self.user = user
        self.payments = payments

    @classmethod
    async def load(cls, tr_uid: str):
        conn = await connect()
        payments = await conn.fetchrow("SELECT * FROM payments WHERE transaction_uid = $1", tr_uid)
        user = await conn.fetchrow("SELECT * FROM users WHERE tg_id = $1", payments["user_id"])
        log.debug("get user and payment db data")
        return cls(user["tg_id"], user, payments)

    @classmethod
    async def add(cls, tg_id: int, t_unid: str, title: str):
        conn = await connect()
        try:
            await conn.execute(
                """
                INSERT INTO payments
                (user_id, transaction_uid, title)
                VALUES
                ($1, $2, $3)
            """,
                tg_id,
                t_unid,
                title,
            )
            log.debug(f"Add payment {tg_id}")
        except AttributeError:
            await conn.execute(
                """
                INSERT INTO payments
                (user_id, transaction_uid)
                VALUES
                ($1, $2, $3)
            """,
                tg_id,
                t_unid,
            )
            log.error("error in add payment")
        finally:
            await conn.close()

    async def refund(cls, tr_uid: str):
        conn = await connect()
        await conn.execute("UPDATE payments SET closed = True WHERE transaction_uid = $1", tr_uid)
        log.debug(f"Payment closed {tr_uid}")
        await conn.close()


# operation static class with balance
class Balance:
    @staticmethod
    async def change(tg_id, amount):
        conn = await connect()
        user = await conn.fetchrow("SELECT * FROM users WHERE tg_id = $1", tg_id)
        await conn.execute("UPDATE users SET full_balance = $1 WHERE tg_id = $2", amount, tg_id)
        log.debug(f"Edit balance {user['tg_id']}")
        await conn.close()


# operation static class with user
class Edit:
    @staticmethod
    async def time_zone(tg_id, action):
        conn = await connect()
        await conn.execute("UPDATE users SET time_zone = $1 WHERE tg_id = $2", action, tg_id)
        log.debug(f"time_zone changed on {action}")
        await conn.close()

    @staticmethod
    async def value(tg_id, action):
        conn = await connect()
        await conn.execute("UPDATE users SET value = $1 WHERE tg_id = $2", action, tg_id)
        log.debug(f"value changed on {action}")
        await conn.close()

    @staticmethod
    async def style(tg_id, style):
        conn = await connect()
        await conn.execute("UPDATE users SET style = $1 WHERE tg_id = $2", style, tg_id)
        log.debug(f"style changed on {style}")
        await conn.close()

    @staticmethod
    async def fiat_amount(tg_id, amount):
        conn = await connect()
        await conn.execute("UPDATE users SET fiat_amount = $1 WHERE tg_id = $2", amount, tg_id)
        log.debug(f"fiat_amount changed on {amount}")
        await conn.close()

    @staticmethod
    async def crypto_amount(tg_id, amount):
        conn = await connect()
        await conn.execute("UPDATE users SET crypto_amount = $1 WHERE tg_id = $2", amount, tg_id)
        log.debug(f"crypto_amount changed on {amount}")
        await conn.close()

    @staticmethod
    async def crypto_max_coins(tg_id, max_value):
        conn = await connect()
        await conn.execute("UPDATE users SET crypto_max_coins = $1 WHERE tg_id = $2", max_value, tg_id)
        log.debug(f"crypto_max_coins changed on {max_value}")
        await conn.close()

    # extend koopeika premium
    @staticmethod
    async def premium_extend(tg_id: int, days=30):
        conn = await connect()
        user_obj = await SelectUser.load(tg_id)
        premium_user = await user_obj.premium()
        if premium_user:
            old_premium_until = user_obj.user["premium_until"]
        else:
            old_premium_until = datetime.utcnow()
        new_premium_until = old_premium_until + timedelta(days=days)
        await conn.execute("UPDATE users SET premium_until = $1 WHERE tg_id = $2", new_premium_until, tg_id)
        log.debug(f"{tg_id} premium until changed on {new_premium_until}")
        await conn.close()

        return new_premium_until

    @staticmethod
    async def premium_refund(tg_id: int, unid: str):
        conn = await connect()
        user = await conn.fetchrow("SELECT * FROM users WHERE tg_id = $1", tg_id)
        payments = await conn.fetchrow("SELECT * FROM payments WHERE transaction_uid = $1", unid)
        title = payments["title"]
        if title:
            if title.startswith("premium_stars_"):
                days = int(title.split("_")[-1])
        else:
            days = 30
            log.error(f"title not found: {unid}")

        old_premium_until = user["premium_until"]
        new_premium_until = old_premium_until - timedelta(days=days)
        await conn.execute("UPDATE users SET premium_until = $1 WHERE tg_id = $2", new_premium_until, tg_id)
        await conn.execute("UPDATE payments SET closed = True WHERE transaction_uid = $1", unid)
        log.debug(f"{user['tg_id']} premium until has been refunded on {new_premium_until}")
        await conn.close()

        return new_premium_until
