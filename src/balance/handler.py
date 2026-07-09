from aiogram.types import CallbackQuery

from config import conf, profile
from users import user_req

from conversion import conv_balance
from tasks.logger import log
from keyboards import dinamic_assets


async def balance_handler(callback: CallbackQuery):
    # init user
    user_id = callback.from_user.id
    con = await conv_balance.con_balance(user_id, conf.rates)
    user_obj = await user_req.load(user_id)
    user = user_obj.user

    # get data
    value = user.get("value")
    style = user.get("style")
    value = conf.values_symbols[style].get(value, f" {value}")

    # update profile
    prof = profile.get(user_id)
    prof.assets_balance = con.assets_balance
    prof.assets_share = con.assets_share

    log.debug(f"Check balance {user_id}")
    await callback.message.edit_text(
        f"Ваш баланс активов – <b>{con.balance}{value}</b>\n"
        f"Добавить актив можно, нажав на кнопку в клавиатуре бота.",
        reply_markup=dinamic_assets
    )
