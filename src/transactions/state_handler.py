from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import transaction_state
from core.exceptions import BadUserIdError, BadMessageText, BigNumError
from users import user_req
from transactions import transaction_req
from config import profile

from utils import checker_num, checker_id
from middlewares.logger import log
from base.keyboard import main_menu


router = Router()


# operations with Transaction
@router.message(transaction_state.edit)
async def transaction_edit(message: Message, state: FSMContext):
    try:
        # get data
        prof = profile.get(message.from_user.id)
        user_obj = await user_req.load(message.from_user.id)
        premium_user = await user_obj.premium()
        user = user_obj.user

        # check data
        await checker_num(message.text, user["value"], premium_user)

        # set state
        prof.choise = float(message.text)
        await state.set_state(transaction_state.edit_end)
        await message.answer("Напишите айди транзакции:")

    except BadMessageText as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)
        await state.clear()
    except BigNumError as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)
        await state.clear()


@router.message(transaction_state.edit_end)
async def transaction_edit_result(message: Message, state: FSMContext):
    try:
        # get data
        prof = profile.get(message.from_user.id)
        num_id = int(message.text)
        amount = prof.choise
        transaction = await transaction_req.load(message.from_user.id)

        # edit transaction
        await transaction.edit(value=amount, num_id=num_id)
        await message.answer("Транзакция успешно изменена!", reply_markup=main_menu)
        log.debug(f"Edit transaction {message.from_user.id}")

    except BadUserIdError as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)
    finally:
        await state.clear()


@router.message(transaction_state.delete)
async def transaction_delete(message: Message, state: FSMContext):
    try:
        num_id = int(message.text)
        transaction = await transaction_req.load(message.from_user.id)

        await transaction.delete(num_id, message.from_user.id)
        await message.answer("Транзакция успешно удалена!", reply_markup=main_menu)
        log.debug(f"Delete transaction {message.from_user.id}")

    except BadUserIdError as ex:
        await message.answer(f"{ex}", reply_markup=main_menu)
    finally:
        await state.clear()
