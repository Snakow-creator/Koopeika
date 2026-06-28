from aiogram import Router, F
from aiogram.types import CallbackQuery

from balance.handler import balance_handler
from transactions.handler import transactions_handler
from assets.handler import assets_handler
from conversion.handler import conversion_handler
from info.handler import list_region_values_handler
from user_profile.handler import profile_info_handler

from base.keyboard import start_keyboard


router = Router()

# functions of services
main_actions = {
    "balance": balance_handler,
    "conversion": conversion_handler,
    "listCurrency": list_region_values_handler,
    "assets": assets_handler,
    "transactions": transactions_handler,
    "profile": profile_info_handler
}


@router.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "Вы перешли в главное меню🏠",
        reply_markup=start_keyboard()
    )


@router.callback_query(F.data.startswith("main_"))
async def callback_main(callback: CallbackQuery):
    await callback.answer()

    action = callback.data.split("_")[1]
    func_handler = main_actions[action] # get function

    await func_handler(callback)
