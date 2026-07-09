from aiogram import Router, F
from aiogram.types import CallbackQuery

from settings import profile_handler, edit_req

from keyboards import con, seg
from tasks.logger import log
from payments.payment import payment_stars
from user_profile.handler import (value_handler, nums_handler,
                                  cryptomaxcoins_handler, premium_handler)

router = Router()


profile_actions = {
    "timezone": profile_handler.change_time_zone,
    "value": value_handler,
    "style": profile_handler.clbk_style,
    "nums": nums_handler,
    "cryptomaxcoins": cryptomaxcoins_handler,
    "premium": premium_handler,
}


@router.callback_query(F.data.startswith("settings_edit_"))
async def settings_action(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]  # input last word in callback_data

    # get function from profile actions
    func = profile_actions[action]
    await func(callback)


@router.callback_query(F.data.startswith("time_zone_"))
async def settings_change_time_zone(callback: CallbackQuery):
    await callback.answer("")
    # get data
    action = callback.data.split("_")[-1]  # input last word in callback_data
    user_id = callback.from_user.id

    text = await profile_handler.time_zone_edit(action, user_id)

    await callback.message.edit_text(text, reply_markup=seg.main_menu())
    log.debug(f"User {user_id} change time zone to {action}")


@router.callback_query(F.data.startswith("style_"))
async def settings_change_style(callback: CallbackQuery):
    await callback.answer("")
    # get data
    action = callback.data.split("_")[-1]  # input last word in callback_data
    user_id = callback.from_user.id

    if action == "symbols":
        await edit_req.style(user_id, "symbols")
        await callback.message.edit_text(
            "Вы сменили стиль на <b>Символы</b>", reply_markup=seg.main_menu()
        )

    elif action == "codename":
        await edit_req.style(user_id, "codename")
        await callback.message.edit_text(
            "Вы сменили стиль на <b>Названия</b>", reply_markup=seg.main_menu()
        )

    log.debug(f"User {user_id} change style to {action}")


@router.callback_query(F.data.startswith("amount_edit_"))
async def settings_choise_amount(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]

    if action == "fiat":
        await callback.message.edit_text(
            "Укажите количество цифр после точки(фиат):", reply_markup=seg.choise_fiat_amount()
        )

    elif action == "crypto":
        await callback.message.edit_text(
            "Укажите количество цифр после точки(криптовалюта):", reply_markup=seg.choise_crypto_amount()
        )


@router.callback_query(F.data.startswith("fiat_amount_"))
async def settings_set_fiat_amount(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]

    await profile_handler.fiat_amount_edit(
        int(action), callback.from_user.id
      )
    await callback.message.edit_text(
        f"Вы изменили количество цифр после запятой(фиат) на <b>{action}</b>",
        reply_markup=seg.main_menu()
    )


@router.callback_query(F.data.startswith("crypto_amount_"))
async def settings_set_crypto_amount(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]

    await profile_handler.crypto_amount_edit(
        int(action), callback.from_user.id
    )
    await callback.message.edit_text(
        f"Вы изменили количество цифр после запятой(криптовалюта) на <b>{action}</b>",
        reply_markup=seg.main_menu()
    )


# edit crypto max coins
@router.callback_query(F.data.startswith("crypto_max_"))
async def settings_set_cryptomaxcoins(callback: CallbackQuery):
    await callback.answer("")
    action = int(callback.data.split("_")[-1])

    text = await profile_handler.crypto_max_coins_edit(
        action, callback.from_user.id
    )
    await callback.message.edit_text(text, reply_markup=seg.main_menu())


@router.callback_query(F.data.startswith("pay_premium_stars_"))
async def pay_premium_month(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-2]

    if action == "stars":
        days = callback.data.split("_")[-1]
        await payment_stars(callback, int(days))

