from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import profile, conf

from keyboards import back_to_balance

router = Router(name="balance")


@router.callback_query(F.data == "balance_dinamic_assets")
async def dinamic_asstes(callback: CallbackQuery):
    await callback.answer()

    text = "Информация о активах:\n\n"

    user_id = callback.from_user.id
    prof = profile.get(user_id)
    assets_balance = prof.assets_balance
    assets_share = prof.assets_share

    # update text
    for asset, amount in assets_balance.items():
        text += f"{amount} <b>{asset}</b> – <b>{assets_share[asset]}%</b>\n"

    await callback.message.edit_text(text, reply_markup=back_to_balance)


