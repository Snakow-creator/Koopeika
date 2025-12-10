from datetime import datetime
from zoneinfo import ZoneInfo

from models.models import User, Transaction
from users.request import Users
from core.request import connect

from core.exceptions import BigCommentError, ManyTransactionsError
from utils.verification import checker_id
from middlewares.logger import log


class Transactions(Users):
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
