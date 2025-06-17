from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache


class AntiFloodMiddleware(BaseMiddleware):

    def __init__(self, timelimit: float = 0.5) -> None:
        self.limit = TTLCache(maxsize=10000, ttl=timelimit)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.id in self.limit:
            return  # возвращаем None если запросы(сообщения) приходят слишком быстро
        else:
            self.limit[event.chat.id] = None
            return await handler(event, data)
