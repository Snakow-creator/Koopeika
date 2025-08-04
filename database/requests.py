from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from operations.verification import checker_id
from database.models import Transaction, User, async_session, AsyncAttrs
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
                user = User(tg_id=tg_id, full_balance=0, time_zone="+3", value="USD", style="symbols")
                session.add(user)
                log.debug(f"Add user {tg_id}")
                await session.commit()
            return cls(tg_id, user, session)



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

    async def add(self, value, assets, description):
        if len(description) >= 30:
            raise BigCommentError()

        # если транзакции больше 50 - выдаем ошибку
        if len(list(self.transactions)) == 50:
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
