from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import desc, select

from commands.functions import checker_id
from database.models import Transaction, User, async_session
from database.errors_config import ManyTransactionsError
from loggers.logs import log


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
            assert len(description) <= 30
            transactions = await Transactions.history_transactions(tg_id)
            # если транзакции больше 50 - выдаем ошибку
            if len(list(transactions)) == 50:
                raise ManyTransactionsError()

            stmt = await session.scalar(select(User).where(User.tg_id == tg_id))
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
            await checker_id(tg_id, num_id)

            await session.commit()

    @staticmethod
    async def delete(tg_id: int, num_id: int):
        async with async_session() as session:
            transaction = await session.scalar(select(Transaction).where(Transaction.id == num_id))
            await checker_id(tg_id, num_id)
            transaction.user_id = f"{transaction.user_id}*"

            await session.commit()


# добавление юзера в бд(команда старт)
async def add_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, full_balance=0, time_zone="+3", value="USD", style="symbols"))
            log.debug(f"Add user {tg_id}")
            await session.commit()


async def user_get(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        return user


async def get_value(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        return user.value


async def get_style(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        return user.style


async def get_time_zone(tg_id: int):
    async with async_session() as session:
        user = await async_session().scalar(select(User).where(User.tg_id == tg_id))

        return user.time_zone


async def get_fiat_amount(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        return user.fiat_amount


async def get_crypto_amount(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        return user.crypto_amount


async def time_zone_edit(action, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.time_zone = action

        await session.commit()


# операции с валютой по умолчанию
async def value_edit(action, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.value = action

        await session.commit()


async def style_edit(style, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.style = style

        await session.commit()


async def fiat_amount_edit(amount, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.fiat_amount = amount

        await session.commit()


async def crypto_amount_edit(amount, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.crypto_amount = amount

        await session.commit()



