from models.models import User, Payment
from users.request import Users

from core.request import connect

from middlewares.logger import log


class Payments(Users):
    def __init__(self, tg_id: int, user: User, payments: Payment):
        self.user_id = tg_id
        self.user = user
        self.payments = payments

    @classmethod
    async def load(cls, tr_uid: str):
        conn = await connect()
        payments = await conn.fetchrow("SELECT * FROM payments WHERE transaction_uid = $1", tr_uid)
        user = await conn.fetchrow("SELECT * FROM users WHERE tg_id = $1", payments["user_id"])
        log.debug("get user and payment db data")
        return cls(user["tg_id"], user, payments)

    @classmethod
    async def add(cls, tg_id: int, t_unid: str, title: str):
        conn = await connect()
        try:
            await conn.execute(
                """
                INSERT INTO payments
                (user_id, transaction_uid, title)
                VALUES
                ($1, $2, $3)
            """,
                tg_id,
                t_unid,
                title,
            )
            log.debug(f"Add payment {tg_id}")
        except AttributeError:
            await conn.execute(
                """
                INSERT INTO payments
                (user_id, transaction_uid)
                VALUES
                ($1, $2, $3)
            """,
                tg_id,
                t_unid,
            )
            log.error("error in add payment")
        finally:
            await conn.close()

    async def refund(cls, tr_uid: str):
        conn = await connect()
        await conn.execute("UPDATE payments SET closed = True WHERE transaction_uid = $1", tr_uid)
        log.debug(f"Payment closed {tr_uid}")
        await conn.close()
