from datetime import datetime, timezone

from models.models import User, user_obj
from core.request import connect
from config.models import bu

from middlewares.logger import log


class Users:
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
                (
                    tg_id, full_balance, time_zone, value,
                    style, fiat_amount, crypto_amount, crypto_max_coins
                )
                VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
                tg_id,
                "0",
                "+3",
                "USD",
                "symbols",
                bu.fiat_amount,
                bu.crypto_amount,
                bu.crypto_max_coins,
            )
            log.debug(user_obj.fiat_amount)
            log.debug(f"Add user {tg_id}")
            await conn.close()
            return await cls.load(tg_id)
        return cls(tg_id, user)

    async def premium(self):
        if self.user["premium_until"] > datetime.utcnow():
            return "premium"
        return False
