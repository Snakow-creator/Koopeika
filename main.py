import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types.error_event import ErrorEvent
from apscheduler import AsyncScheduler

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from commands import callbacks, handlers, states
from commands.schedulers import const_rates, const_cryptorates
from database.models import async_main
from loggers.antiflood import AntiFloodMiddleware
from loggers.check_subscribe import CheckSubscribtion
from loggers.logs import start_logging, log
from secret.config import BOT_PROPERTIES, TOKEN

bot = Bot(token=TOKEN, default=BOT_PROPERTIES)
dp = Dispatcher()


@dp.error()
async def global_error_handler(event: ErrorEvent) -> None:
    log.error(f"{event.exception}", exc_info=True)


async def main() -> None:
    async with AsyncScheduler() as scheduler:

        dp.message.middleware(AntiFloodMiddleware())
        dp.include_routers(handlers.router, callbacks.router, states.router)

        await scheduler.start_in_background()
        await scheduler.add_schedule(const_rates, CronTrigger(hour=0, minute=0), id="const_rates")
        await scheduler.add_schedule(const_cryptorates, IntervalTrigger(hours=1), id="const_cryptorates")

        start_logging()
        await async_main()
        await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.error("Exit")
