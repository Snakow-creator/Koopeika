from datetime import datetime, timedelta

from core.request import connect
from users import user_req

from middlewares.logger import log


# operation static class with user
class EditRequest:
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
        # connect and init user
        conn = await connect()
        user_obj = await user_req.load(tg_id)
        premium_user = await user_obj.premium()

        # set is premium user or not
        # if premium user get old premium until
        # else get current time
        if premium_user:
            old_premium_until = user_obj.user["premium_until"]
        else:
            old_premium_until = datetime.utcnow()
        new_premium_until = old_premium_until + timedelta(days=days)

        # set premium
        await conn.execute("UPDATE users SET premium_until = $1 WHERE tg_id = $2", new_premium_until, tg_id)
        log.debug(f"{tg_id} premium until changed on {new_premium_until}")
        await conn.close()

        return new_premium_until

    @staticmethod
    async def premium_refund(tg_id: int, unid: str):
        # connect and init user, title
        conn = await connect()
        user = await conn.fetchrow("SELECT * FROM users WHERE tg_id = $1", tg_id)
        payments = await conn.fetchrow("SELECT * FROM payments WHERE transaction_uid = $1", unid)
        title = payments["title"]

        # get days
        if title:
            if title.startswith("premium_stars_"):
                days = int(title.split("_")[-1])
        else:
            days = 30
            log.error(f"title not found: {unid}")

        # refund old time premium to user
        old_premium_until = user["premium_until"]
        new_premium_until = old_premium_until - timedelta(days=days)

        await conn.execute("UPDATE users SET premium_until = $1 WHERE tg_id = $2", new_premium_until, tg_id)
        await conn.execute("UPDATE payments SET closed = True WHERE transaction_uid = $1", unid)
        log.debug(f"{user['tg_id']} premium until has been refunded on {new_premium_until}")
        await conn.close()

        return new_premium_until
