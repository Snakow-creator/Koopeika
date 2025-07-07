from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import desc, select

from operations.verification import checker_id
from database.models import Transaction, User, async_session
from database.errors_config import ManyTransactionsError, BigCommentError
from loggers.logs import log


# добавление юзера в бд(команда старт)
async def add_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, full_balance=0, time_zone="+3", value="USD", style="symbols"))
            log.debug(f"Add user {tg_id}")
            await session.commit()


# класс операций связанных с балансом
class Balance:

    @staticmethod
    async def edit(tg_id, amount) -> None:
        async with async_session() as session:
            stmt = await session.scalar(select(User).where(User.tg_id == tg_id))
            stmt.full_balance = amount
            log.debug(f"Edit balance {tg_id}")
            await session.commit()


# класс операций связанных с транзакциями
class Transactions:

    # отправление запроса для получения транзакций юзера
    @staticmethod
    async def history_transactions(tg_id: int):
        async with async_session() as session:
            return await session.scalars(
                select(Transaction).where(Transaction.user_id == tg_id).order_by(desc(Transaction.id))
            )

    @staticmethod
    async def add(value: str, tg_id: int, assets: str, description: str):
        async with async_session() as session:
            if len(description) <= 30:
                raise BigCommentError()
            # если транзакции больше 50 - выдаем ошибку
            if len(list(transactions)) == 50:
                raise ManyTransactionsError()

            transactions = await Transactions.history_transactions(tg_id)
            stmt = await Get.user(tg_id)
            time = datetime.now(ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d %H:%M")
            session.add(
                Transaction(
                    value=value,
                    user=stmt,
                    amount=assets,
                    time=time,
                    description=description,
                )
            )

            await session.commit()

    @staticmethod
    async def edit(value: float, tg_id: int, num_id: int):
        async with async_session() as session:
            transaction = await session.scalar(select(Transaction).where(Transaction.id == num_id))
            op = transaction.amount[0]
            transaction.amount = op + f"{str(value)}"
            user_transaction = await Transactions.history_transactions(tg_id)
            await checker_id(num_id, user_transaction)

            await session.commit()

    @staticmethod
    async def delete(tg_id: int, num_id: int):
        async with async_session() as session:
            transaction = await session.scalar(select(Transaction).where(Transaction.id == num_id))
            user_transaction = await Transactions.history_transactions(tg_id)
            await checker_id(num_id, user_transaction)
            transaction.user_id = f"{transaction.user_id}*"

            await session.commit()


class Get:
    @staticmethod
    async def user(tg_id: int):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            return user

    @staticmethod
    async def value(tg_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            return user.value

    @staticmethod
    async def style(tg_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            return user.style

    @staticmethod
    async def time_zone(tg_id: int):
        async with async_session() as session:
            user = await async_session().scalar(select(User).where(User.tg_id == tg_id))

            return user.time_zone

    @staticmethod
    async def fiat_amount(tg_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            return user.fiat_amount

    @staticmethod
    async def crypto_amount(tg_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            return user.crypto_amount


class Edit:
    @staticmethod
    async def time_zone(action, tg_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.time_zone = action

            await session.commit()

    # операции с валютой по умолчанию
    @staticmethod
    async def value(action, tg_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.value = action

            await session.commit()

    @staticmethod
    async def style(style, tg_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.style = style

            await session.commit()

    @staticmethod
    async def fiat_amount(amount, tg_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.fiat_amount = amount

            await session.commit()

    @staticmethod
    async def crypto_amount(amount, tg_id):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            user.crypto_amount = amount

            await session.commit()
