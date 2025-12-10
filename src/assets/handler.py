from aiogram.types import CallbackQuery

from keyboards import assets


async def assets_handler(callback: CallbackQuery):
    await callback.message.edit_text('Выберите нужное <b>действие</b>👇',
                         reply_markup=assets.assets_keyboard())

