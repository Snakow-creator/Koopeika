from aiogram import Bot, Dispatcher
from aiogram.types import ErrorEvent

from apscheduler import AsyncScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from config.secret import TOKEN, BOT_PROPERTIES
from core.request import async_main
from core.routers import router, init_routers

from tasks.logger import log, start_logging
from schedulers.profile_cleanup import profile_cleaner
from middlewares.antiflood import AntiFloodMiddleware

from schedulers.rates import const_rates, dinamic_cryptorates

import asyncio


bot = Bot(token=TOKEN, default=BOT_PROPERTIES)
dp = Dispatcher()

# test
@dp.error()
async def global_error_handler(event: ErrorEvent) -> None:
    log.error(f"{event.exception}", exc_info=True)


async def main():
    async with AsyncScheduler() as scheduler:
        # set middlewares
        dp.message.middleware(AntiFloodMiddleware())

        dp.include_router(router)

        await scheduler.start_in_background()
        await scheduler.add_schedule(const_rates, CronTrigger(hour=0, minute=0), id="const_rates")
        await scheduler.add_schedule(dinamic_cryptorates, IntervalTrigger(minutes=5), id="dinamic_cryptorates")
        await scheduler.add_schedule(profile_cleaner, IntervalTrigger(seconds=10), id="profile_cleaner")

        # start services
        start_logging() # init logger
        await async_main() # init db
        await init_routers() # init routers
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
