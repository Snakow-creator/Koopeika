from aiogram import BaseMiddleware
from aiogram.types import Message

from core.exceptions import ProfileExpiredError
from keyboards import main_menu

from tasks.logger import log


class ProfileExpiredMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)

        except ProfileExpiredError as e:
            log.info(f"ProfileExpiredError caught in middleware for user {getattr(event, 'from_user', None)}")

            bot = data.get("bot")
            if not bot:
                return

            text = "⌛ Похоже, вы давно не пользовались ботом, перейдите в главное меню, чтобы начать заново."

            try:
                if hasattr(event, "callback_query") and event.callback_query:
                    log.debug(f"Edit expired callback query message for user {event.callback_query.from_user.id}")
                    await event.callback_query.message.edit_text(text, reply_markup=main_menu)
                    await event.callback_query.answer()
                elif isinstance(event, Message):          # ← главное изменение
                    # Обычное сообщение
                    log.info(f"Edit expired message for user {event.chat.id}")
                    await event.answer(text, reply_markup=main_menu)
                else:
                    log.warning(f"Неизвестный тип event: {type(event)}")
                    # Fallback через bot
                    if hasattr(event, "bot") and hasattr(event, "chat"):
                        await event.bot.send_message(
                            chat_id=event.chat.id,
                            text=text,
                            reply_markup=main_menu
                        )
            except Exception as send_err:
                log.error(f"Failed to send expired profile message: {send_err}")


            return

        except Exception as e:
            # other exceptions should be raised
            log.exception("Unexpected error in middleware")
            raise e # re-raise, 'cause we don't want to handle it
