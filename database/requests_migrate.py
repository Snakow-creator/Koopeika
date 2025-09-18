from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Transaction, User, Payment, lite_main, async_lite_session, async_main

from secret.config import POSTGRES_DATABASE, POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT

import asyncpg
import asyncio


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


async def migrate():
    await lite_main()
    await async_main()

    async with async_lite_session() as session:
        users = await session.scalars(select(User))
        transactions = await session.scalars(select(Transaction))
        payments = await session.scalars(select(Payment))

        await create_user(users)
        await create_transaction(transactions)
        await create_payments(payments)



async def create_user(users):
    conn = await connect()
    for user in users:
        await conn.execute("""
            INSERT INTO users
            (tg_id, full_balance, registered, premium_until, time_zone, value, style, fiat_amount, crypto_amount, crypto_max_coins)
            VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        """,
            int(user.tg_id),
            user.full_balance,
            user.registered,
            user.premium_until,
            user.time_zone,
            user.value,
            user.style,
            user.fiat_amount,
            user.crypto_amount,
            user.crypto_max_coins,
        )
    await conn.close()


async def create_transaction(transactions):
    conn = await connect()
    for tran in transactions:
        await conn.execute("""
            INSERT INTO transactions
            (user_id, value, amount, time, description, closed)
            VALUES
            ($1, $2, $3, $4, $5, $6)
        """,
            int(tran.user_id),
            tran.value,
            tran.amount,
            tran.time,
            tran.description,
            bool(tran.closed),
        )
    await conn.close()


async def create_payments(payments):
    conn = await connect()
    for payment in payments:
        await conn.execute("""
            INSERT INTO payments
            (user_id, transaction_uid, title, added, closed)
            VALUES
            ($1, $2, $3, $4, $5)
        """,
            int(payment.user_id),
            payment.transaction_uid,
            payment.title,
            payment.added,
            payment.closed,
        )
    await conn.close()
