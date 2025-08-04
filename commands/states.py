from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from operations.verification import checker_num, checker_con_num, int_or_float
from operations.message import delete_message
from loggers.logs import log
from database.errors_config import (
    BadMessageText,
    BadUserIdError,
    ManyTransactionsError,
    BigNumError,
    BigCommentError,
)

import commands.keyboards as kb
import database.online_config as oc
import database.requests as rq

# роутер и личные переменные юзера
router = Router()


# импорты фсм контекста
class Balance(StatesGroup):
    add = State()
    deprive = State()
    assets_end = State()


class Transaction(StatesGroup):
    edit = State()
    edit_end = State()
    delete = State()


class Conversion(StatesGroup):
    input_number = State()


# Conversion
@router.message(Conversion.input_number)
async def con_input_second_number(message: Message, state: FSMContext):
    try:
        await delete_message(message)
        user_id = message.from_user.id
        value = oc.first_con_value[user_id]
        user_obj = await rq.SelectUser.load(user_id)
        user = user_obj.user

        if value == "⭐️":
            keyboard = kb.con.stars_popular_values()
        else:
            keyboard = kb.con.popular_values("endcon")

        await checker_con_num(message.text, value)
        # after checker
        amount = await int_or_float(message.text)
        oc.input_value[user_id] = amount

        await message.answer(
            f"Вы указали: <b>{amount:,}{oc.values_symbols[user.style][value]}</b>."
            f"\nВыберите валюту, в которую требуется конвертировать сумму⬇️",
            reply_markup=keyboard,
        )
    except BadMessageText as ex:
        await message.answer(f"{ex}")

    finally:
        await state.clear()


# operations with balance +
@router.message(Balance.add)
async def add_assets(message: Message, state: FSMContext):
    try:
        value = oc.data_value.get(message.from_user.id, 0)
        await checker_num(message.text, value)
        oc.user_choise[message.from_user.id] = "+" + message.text
        await state.set_state(Balance.assets_end)
        await message.answer(
            "Введите комментарий(максимум <b>30</b> символов):",
            reply_markup=kb.clbk.no_comment(),
        )
    except BadMessageText as ex:
        await message.answer(f"{ex}")
        await state.clear()
    except BigNumError as ex:
        await message.answer(f"{ex}")
        await state.clear()


# operations with balance -
@router.message(Balance.deprive)
async def add_losses(message: Message, state: FSMContext):
    try:
        value = oc.data_value.get(message.from_user.id, 0)
        await checker_num(message.text, value)
        oc.user_choise[message.from_user.id] = "-" + message.text
        await state.set_state(Balance.assets_end)
        await message.answer(
            "Введите комментарий(максимум <b>30</b> символов):",
            reply_markup=kb.clbk.no_comment(),
        )
    except BadMessageText as ex:
        await message.answer(f"{ex}")
        await state.clear()
    except BigNumError as ex:
        await message.answer(f"{ex}")
        await state.clear()


@router.message(Balance.assets_end)
async def add_transaction(message: Message, state: FSMContext):
    try:
        value = oc.data_value.get(message.from_user.id, 0)
        assets = oc.user_choise.get(message.from_user.id, 0)
        description = str(message.text)
        transaction = await rq.Transactions.load(message.from_user.id)
        await transaction.add(value, assets, description)
        await message.answer("Функция произведена успешно✅")
        log.debug(f"Add assets {message.from_user.id}")
    except ManyTransactionsError as ex:
        await message.answer(f"{ex}")
    except BigCommentError as ex:
        await message.answer(f"{ex}")
    finally:
        await state.clear()


# operations with Transaction
@router.message(Transaction.edit)
async def transaction_edit(message: Message, state: FSMContext):
    try:
        user_obj = await rq.SelectUser.load(message.from_user.id)
        user = user_obj.user
        await checker_num(message.text, user.value)
        oc.user_choise[message.from_user.id] = float(message.text)
        await state.set_state(Transaction.edit_end)
        await message.answer("Напишите айди транзакции:")
    except BadMessageText as ex:
        await message.answer(f"{ex}")
        await state.clear()
    except BigNumError as ex:
        await message.answer(f"{ex}")
        await state.clear()


@router.message(Transaction.edit_end)
async def transaction_edit_result(message: Message, state: FSMContext):
    try:
        num_id = int(message.text)
        amount = oc.user_choise.get(message.from_user.id)
        transaction = await rq.Transactions.load(message.from_user.id)
        await transaction.edit(value=amount, num_id=num_id)
        await message.answer("Транзакция успешно изменена!")
        log.debug(f"Edit transaction {message.from_user.id}")
    except BadUserIdError as ex:
        await message.answer(f"{ex}")
    finally:
        await state.clear()


@router.message(Transaction.delete)
async def transaction_delete(message: Message, state: FSMContext):
    try:
        num_id = int(message.text)
        await state.clear()
        transaction = await rq.Transactions.load(message.from_user.id)
        await transaction.delete(num_id)
        await message.answer("Транзакция успешно удалена!")
        log.debug(f"Delete transaction {message.from_user.id}")
    except BadUserIdError as ex:
        await message.answer(f"{ex}")
    finally:
        await state.clear()
