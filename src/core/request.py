from models.models import Base, async_engine

from config import settings

import asyncpg


# function needed for work
async def async_main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def connect():
    pd = settings.postgres_data
    # подключение к базе данных
    conn = await asyncpg.connect(
        user=pd["user"],
        password=pd["password"],
        database=pd["database"],
        host=pd["host"],
        port=pd["port"],
    )
    return conn
