from aiogram.types import CallbackQuery

from keyboards import info_regions


async def list_region_values_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Выберите регион страны</b>,\nкод валюты которой вы желаете посмотреть.\n"
        "Или вы можете выбрать <b>Популярные валюты</b> и <b>Криптовалюты</b>.",
        reply_markup=info_regions(),
    )
