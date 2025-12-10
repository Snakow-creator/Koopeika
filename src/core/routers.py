from aiogram import Router

from middlewares.logger import log

from base.message import router as base_handler_router
from base.callback import router as base_callback_router

from balance.callback import router as balance_router
from conversion.callback import router as conversion_router
from transactions.callback import router as transaction_router
from assets.callback import router as assets_router
from info.callback import router as info_router
from user_profile.callback import router as profile_router
from payments.callback import router as payments_router

from assets.state_handler import router as assets_state_router
from conversion.states_handler import router as conversion_state_router
from transactions.state_handler import router as transaction_state_router
from payments.handler import router as payments_handler_router


router = Router(name="init_router")


routers = [
    base_handler_router,
    base_callback_router,

    balance_router,
    transaction_router,
    conversion_router,
    assets_router,
    info_router,
    profile_router,
    payments_router,

    assets_state_router,
    conversion_state_router,
    transaction_state_router,
    payments_handler_router,
]


async def init_routers():
    router.include_routers(*routers)

    log.debug("Routers initialized")
