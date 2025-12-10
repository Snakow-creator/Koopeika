from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache


class AntiFloodMiddleware(BaseMiddleware):

    def __init__(self) -> None:
        # хранит максимум 10000 элементов
        # время жизни элемента полсекунды, потом автоматом удаляется
        self.limit = TTLCache(maxsize=10000, ttl=0.5)

    # не проталкивает сообщение, если оно приходит слишком быстро
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
