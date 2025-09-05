from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from operations.verification import checker_id
from database.models import Transaction, User, Payment, async_session, AsyncAttrs
from database.errors_config import ManyTransactionsError, BigCommentError
from loggers.logs import log


class SelectUser:
    def __init__(self, tg_id: int, user: User, session: AsyncSession):
        self.id = tg_id
        self.user = user
        self.session = session

    @classmethod
    async def load(cls, tg_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            if not user:
                user = User(
                    tg_id=tg_id,
                    full_balance=0,
                    time_zone="+3",
                    value="USD",
                    style="symbols",
                    registered=datetime.now(timezone.utc),
                    premium_until=datetime.now(timezone.utc),
                )
                session.add(user)
                log.debug(f"Add user {tg_id}")
                await session.commit()
            return cls(tg_id, user, session)

    async def premium(self):
        if self.user.premium_until > datetime.utcnow():
            return "premium"
        return False


class Transactions(SelectUser):
    def __init__(self, tg_id, user: User, transactions: Transaction, session: AsyncSession):
        self.id = tg_id
        self.user = user
        self.transactions = transactions
        self.session = session

    @classmethod
    async def load(cls, tg_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            transactions = await session.scalars(
                select(Transaction).where(Transaction.user_id == tg_id).order_by(desc(Transaction.id))
            )
            log.debug("get user and transaction db data")
            return cls(tg_id, user, transactions, session)

    @staticmethod
    async def get_values():
        async with async_session() as session:
            values = await session.scalars(select(Transaction.value).distinct())
            log.debug(f"Get rq_values {list(values)}")
            return list(values)

    async def add(self, value, assets, description):
        if len(description) >= 30:
            raise BigCommentError()

        # если транзакции больше 50 - выдаем ошибку
        max_trs = 50
        if self.user.premium_until > datetime.utcnow():
            max_trs = 300

        if len(list(self.transactions)) == max_trs:
            raise ManyTransactionsError()

        time = datetime.now(ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d %H:%M")
        self.session.add(
            Transaction(
                value=value,
                user=self.user,
                amount=assets,
                time=time,
                description=description,
            )
        )
        log.debug(f"Add transaction {self.user.id}")
        await self.session.commit()

    async def edit(self, value: float, num_id: int):
        transaction = await self.session.scalar(select(Transaction).where(Transaction.id == num_id))
        op = transaction.amount[0]  # get operation amount + or -
        transaction.amount = op + f"{str(value)}"
        await checker_id(num_id, self.transactions)
        log.debug(f"Edit transaction {num_id}")
        await self.session.commit()

    async def delete(self, num_id: int):
        transaction = await self.session.scalar(select(Transaction).where(Transaction.id == num_id))
        await checker_id(num_id, self.transactions)
        transaction.user_id = f"{transaction.user_id}*"
        log.debug(f"Delete transaction {num_id}")
        await self.session.commit()


class Payments(SelectUser):
    def __init__(self, tg_id: int, user: User, payments: Payment, session: AsyncSession):
        self.user_id = tg_id
        self.user = user
        self.session = session
        self.payments = payments

    @classmethod
    async def load(cls, tr_uid: str):
        async with async_session() as session:
            payments = await session.scalar(select(Payment).where(Payment.transaction_uid == tr_uid))
            user = await session.scalar(select(User).where(User.tg_id == payments.user_id))
            log.debug("get user and payment db data")
            return cls(user.tg_id, user, payments, session)

    @classmethod
    async def add(cls, tg_id: int, t_unid: str):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            session.add(
                Payment(
                    user=user,
                    transaction_uid=t_unid
                )
            )
            log.debug(f"Add payment {tg_id}")
            await session.commit()

    async def refund(cls, tr_uid: str):
        async with async_session() as session:
            payments = await session.scalar(select(Payment).where(Payment.transaction_uid == tr_uid))
            payments.closed = True
            log.debug(f"Payment closed {tr_uid}")
            await session.commit()


# operation static class with balance
class Balance:
    @staticmethod
    async def change(tg_id, amount):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.full_balance = amount
            log.debug(f"Edit balance {user.id}")
            await session.commit()


# operation static class with user
class Edit:
    @staticmethod
    async def time_zone(tg_id, action):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.time_zone = action
            log.debug(f"time_zone changed on {action}")
            await session.commit()

    @staticmethod
    async def value(tg_id, action):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.value = action
            log.debug(f"value changed on {action}")
            await session.commit()

    @staticmethod
    async def style(tg_id, style):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.style = style
            log.debug(f"style changed on {style}")
            await session.commit()

    @staticmethod
    async def fiat_amount(tg_id, amount):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.fiat_amount = amount
            log.debug(f"fiat_amount changed on {amount}")
            await session.commit()

    @staticmethod
    async def crypto_amount(tg_id, amount):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.crypto_amount = amount
            log.debug(f"crypto_amount changed on {amount}")
            await session.commit()

    @staticmethod
    async def crypto_max_coins(tg_id, max_value):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.crypto_max_coins = max_value
            log.debug(f"crypto_max_coins changed on {max_value}")
            await session.commit()

    # extend koopeika premium
    @staticmethod
    async def month_premium_extend(tg_id: int):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user_obj = await SelectUser.load(tg_id)
            premium_user = await user_obj.premium()
            if premium_user:
                old_premium_until = user.premium_until
            else:
                old_premium_until = datetime.now(timezone.utc)
            new_premium_until = old_premium_until + timedelta(days=30)
            user.premium_until = new_premium_until
            log.debug(f"{user.tg_id} premium until changed on {new_premium_until}")
            await session.commit()

            return new_premium_until

    @staticmethod
    async def month_premium_refund(tg_id: int, unid: str):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            payments = await session.scalar(select(Payment).where(Payment.transaction_uid == unid))
            old_premium_until = user.premium_until
            new_premium_until = old_premium_until - timedelta(days=30)
            user.premium_until = new_premium_until
            payments.closed = True
            log.debug(f"{user.tg_id} premium until has been refunded on {new_premium_until}")
            await session.commit()

            return new_premium_until
