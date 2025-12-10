from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import conf
from keyboards import pay


router = Router(name="payments")


@router.callback_query(F.data == "terms_of_service")
async def terms_of_service(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text(conf.terms_of_service, reply_markup=pay.terms_of_services_back())
