from aiogram.types import CallbackQuery

from users import user_req
from config import profile

from settings import profile_handler
from keyboards import seg, con, pay


async def profile_info_handler(callback: CallbackQuery):
    await callback.answer("")

    # get user data
    user_obj = await user_req.load(callback.from_user.id)
    premium_user = await user_obj.premium()

    text_info = await profile_handler.user_info(
        premium_user, callback.from_user.id
    )
    await callback.message.edit_text(
        text_info, reply_markup=seg.settings(premium_user)
    )


# handlers for edit profile
async def value_handler(callback: CallbackQuery):
    # get user data
    user_id = callback.from_user.id
    user_obj = await user_req.load(user_id)
    premium_user = await user_obj.premium()
    # change choise for assets handler
    profile.get(user_id).choise = "edit"

    if premium_user:
        keyboard = con.popular_values(premium_user)
    else:
        keyboard = seg.classic_values()

    await callback.message.edit_text("Выберите валюту по умолчанию:", reply_markup=keyboard)


async def nums_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите у каких активов вы хотите изменить кол-во десятичных знаков⬇️",
        reply_markup=seg.choise_amount(),
    )


async def cryptomaxcoins_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите размер списка криптовалют⬇️",
        reply_markup=seg.crypto_max_coins(),
    )


async def premium_handler(callback: CallbackQuery):
    await callback.message.edit_text(
            "Хотите получить больше возможностей и валют?\n\n"
            "Купите <b>Koopeika Premium</b> и откройте возможности:\n"
            "1. Выбор до 48 криптовалют\n"
            "2. Выбор <b>криптовалют</b> и <b>Telegram Stars</b> по умолчанию\n"
            "3. Конвертация из звезд в криптовалюту\n"
            "4. Лимит до 300 транзакций(по умолчанию 50)\n"
            "5. Увеличен лимит на сумму валют в 1000 раз",
            reply_markup=pay.premium_buttons(),
        )
