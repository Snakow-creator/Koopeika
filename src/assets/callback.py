from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from config import profile
from users import user_req
from transactions import transaction_req

from keyboards import con, seg
from base.keyboard import main_menu
from tasks.logger import log
from states import balance_state
from core.exceptions import ManyTransactionsError

from utils import choise_value
from settings import profile_handler


router = Router()


# add assets or deprive
@router.callback_query(F.data.startswith("add_assets_"))
async def add_assets(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]

    user_obj = await user_req.load(callback.from_user.id)
    premium = await user_obj.premium()
    prof = profile.get(callback.from_user.id, create=True)
    prof.choise = action
    prof.text = "Укажите <b>валюту</b>:"
    await callback.message.edit_text(
        "Укажите <b>валюту</b>:",
        reply_markup=con.popular_values(premium, convertation=False),
    )


# input popular and full list values, for classic values list smaller
@router.callback_query(F.data.startswith("add_value_"))
async def add_transaction(callback: CallbackQuery, state: FSMContext):
    value = callback.data.split("_")[-1]  # input last 3 letters of code value

    prof = profile.get(callback.from_user.id)
    choise = prof.choise  # change or deprive or edit
    answer_, text = await choise_value(value)  # format value
    prof.value = value
    log.debug(f"choise: {choise}")

    await callback.answer(answer_)

    op = {"change": "накопления", "deprive": "траты"}

    if choise in ("change", "deprive"):
        await state.set_state(balance_state.change)
        await callback.message.edit_text(
            text
            + f"\nУкажите ваши {op[choise]} в сообщения(дробные числа указываются точкой):"
        )

    elif choise == "edit":
        text = await profile_handler.default_value_edit(value, callback.from_user.id)
        await callback.message.edit_text(text, reply_markup=seg.main_menu())


# выполняем функцию отвечающую на кнопку "Без комментариев"
@router.callback_query(F.data == "without_comment")
async def add_transaction_without_comment(callback: CallbackQuery, state: FSMContext):
    try:
        # get data
        prof = profile.get(callback.from_user.id)
        value, choise = prof.value, prof.choise

        # add transaction in db
        transaction = await transaction_req.load(callback.from_user.id)
        await transaction.add(value, choise, "")
        log.debug(f"Add assets {callback.from_user.id}")

        await callback.message.edit_text(
            "Функция произведена успешно.", reply_markup=main_menu
        )

    except ManyTransactionsError as ex:
        await callback.message.edit_text(str(ex), reply_markup=main_menu)

    finally:
        await state.clear()
