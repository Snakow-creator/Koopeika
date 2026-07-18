from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from users import user_req
from transactions import transaction_req
from config import profile

from states import balance_state
from keyboards import assets
from base.keyboard import main_menu
from tasks.logger import log
from core.exceptions import (
    BadMessageText,
    BigNumError,
    ManyTransactionsError,
    BigCommentError,
)

from utils import checker_num, checker_value, choise_value
from settings import profile_handler


router = Router(name="assets_state")


# balance input crypto
@router.message(balance_state.input_crypto)
async def balance_input_crypto(message: Message, state: FSMContext):
    user_value = message.text.upper()
    log.debug(user_value)
    value = await checker_value(user_value)


    prof = profile.get(message.from_user.id)
    choise = prof.choise
    log.debug(f"choise: {choise}")
    answer_, text = await choise_value(value)
    prof.value = value

    op = {"change": "накопления", "deprive": "траты"}

    if choise in ("change", "deprive"):
        await state.set_state(balance_state.change)
        await message.answer(
            text
            + f"\nУкажите ваши {op[choise]} в сообщения(дробные числа указываются точкой):"
        )

    elif choise == "edit":
        text = await profile_handler.default_value_edit(value, message.from_user.id)
        await message.answer(text)


# operations with balance +
@router.message(balance_state.change)
async def add_assets(message: Message, state: FSMContext):
    try:
        user = await user_req.load(message.from_user.id)
        premium_user = await user.premium()

        prof = profile.get(message.from_user.id)
        # check num is correct in limits
        await checker_num(message.text, prof.value, premium_user)

        op = {
            "change": "+",
            "deprive": "-",
        }
        chs = prof.choise
        prof.choise = op[chs] + message.text
        log.debug(f"assets: {chs}, {prof.choise}")

        await state.set_state(balance_state.assets_end)
        await message.answer(
            "Введите комментарий(максимум <b>30</b> символов):",
            reply_markup=assets.no_comment(),
        )

    except BadMessageText as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)
        await state.clear()

    except BigNumError as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)
        await state.clear()


@router.message(balance_state.assets_end)
async def add_transaction(message: Message, state: FSMContext):
    try:
        # get data
        prof = profile.get(message.from_user.id)
        value, choise = prof.value, prof.choise
        description = str(message.text)

        # add transaction in db
        transaction = await transaction_req.load(message.from_user.id)
        await transaction.add(value, choise, description)
        log.debug(f"Add assets {message.from_user.id}")

        await message.answer("Функция произведена успешно✅", reply_markup=main_menu)

    except ManyTransactionsError as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)

    except BigCommentError as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)

    finally:
        await state.clear()
