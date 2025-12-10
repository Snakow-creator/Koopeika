from aiogram.types import CallbackQuery

from config import profile
from users import user_req

from keyboards import con



async def conversion_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_obj = await user_req.load(user_id)
    premium = await user_obj.premium()
    prof = profile.get(user_id)
    prof.text = "Укажите валюту, в которую хотите конвертировать:"
    prof.con_value = None
    await callback.message.edit_text(
        "Укажите валюту, в которую хотите конвертировать:",
        reply_markup=con.popular_values(premium, "con"),
    )
