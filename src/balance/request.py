from core.request import connect

from middlewares.logger import log


# operation static class with balance
class Balance:
    @staticmethod
    async def change(tg_id, amount):
        conn = await connect()
        user = await conn.fetchrow("SELECT * FROM users WHERE tg_id = $1", tg_id)
        await conn.execute("UPDATE users SET full_balance = $1 WHERE tg_id = $2", amount, tg_id)
        log.debug(f"Edit balance {user['tg_id']}")
        await conn.close()
