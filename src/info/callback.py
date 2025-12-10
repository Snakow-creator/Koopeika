from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import conf
from keyboards import back_info_regions

from info.handler import list_region_values_handler


router = Router(name="info")


# info regions
@router.callback_query(F.data.startswith("info_"))
async def info_region_value(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]  # Извлекаем последние буквы callback_data
    await callback.message.edit_text(
        text=conf.currency_dict[action],
        reply_markup=back_info_regions(),
        disable_web_page_preview=True,
    )


# back to list region values
@router.callback_query(F.data == "back_to_list_regions")
async def back_to_list_regions(callback: CallbackQuery):
    await list_region_values_handler(callback)
