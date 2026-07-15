from aiogram import BaseMiddleware

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
                    await event.callback_query.message.edit_text(text, reply_markup=main_menu)
                    await event.callback_query.answer()
                elif hasattr(event, "message") and event.message:
                    await event.message.answer(text, reply_markup=main_menu)
            except Exception as send_err:
                log.error(f"Failed to send expired profile message: {send_err}")


            return

        except Exception as e:
            # other exceptions should be raised
            log.exception("Unexpected error in middleware")
            raise e # re-raise, 'cause we don't want to handle it
