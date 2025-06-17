from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

import commands.keyboards as kb


class CheckSubscribtion(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        chat_member = await event.bot.get_chat_member("@obotov", event.from_user.id)

        if chat_member.status == "left":
            await event.answer(
                "Подпишись на канал чтобы пользоваться ботом⬇️", reply_markup=kb.sub_channel
            )
        else:
            return await handler(event, data)
