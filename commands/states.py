from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from database.online_config import Profile
from operations.verification import checker_num, checker_con_num, int_or_float, checker_value
from operations.conversion import Conversion
from operations.choise_value import choise_value
from operations.message import delete_message
from loggers.logs import log
from database.errors_config import (
    BadMessageText,
    BadUserIdError,
    ManyTransactionsError,
    BigNumError,
    BigCommentError,
    ValueNotFoundError
)

import operations.settings as os
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
    input_crypto = State()


class Transaction(StatesGroup):
    edit = State()
    edit_end = State()
    delete = State()


class Con(StatesGroup):
    input_number = State()
    input_crypto = State()


# Conversion
@router.message(Con.input_crypto)
async def input_crypto(message: Message, state: FSMContext):
    try:
        user_value = message.text.upper()
        value = await checker_value(user_value)

        await state.set_state(Con.input_number)  # install state
        user_id = message.from_user.id
        profile = Profile.get(user_id)
        user_obj = await rq.SelectUser.load(user_id)
        user = user_obj.user
        action = profile.con_choise
        if action == "con":
            answer_, text = await choise_value(value)
            profile.con_value = value  # save first value

            oc.msg[user_id] = await message.answer(
                f"{text}\nУкажите количество валюты, которое вы хотите конвертировать:"
                f"\nИли нажмите на число ниже⬇️",
                reply_markup=kb.con.input_numbers(oc.values_symbols[user["style"]].get(value, f" {value}")),
            )
        elif action == "endcon":
            amount = profile.amount
            user_obj = await rq.SelectUser.load(user_id)
            user = user_obj.user

            # get two values and convert it
            first_value = profile.con_value
            result = await Conversion.conversion(user_id, first_value, value, amount, oc.rates)
            from_symbol = oc.values_symbols[user["style"]].get(first_value, f" {first_value}")
            to_symbol = oc.values_symbols[user["style"]].get(value, f" {value}")
            log.debug(f"Conversion {message.from_user.id}")
            await message.answer(result.text(from_symbol, to_symbol))
    except ValueNotFoundError as ex:
        await message.answer(f"{ex}")



@router.message(Con.input_number)
async def con_input_second_number(message: Message, state: FSMContext):
    try:
        await delete_message(message)
        user_id = message.from_user.id
        profile = Profile.get(user_id)
        value = profile.con_value
        user_obj = await rq.SelectUser.load(user_id)
        user = user_obj.user
        premium_user = await user_obj.premium()

        if value == "⭐️":
            keyboard = kb.con.stars_popular_values(premium_user)
        else:
            keyboard = kb.con.popular_values(premium_user, "endcon")

        await checker_con_num(message.text, value, premium_user)
        # after checker
        amount = await int_or_float(message.text)
        profile.amount = amount

        await message.answer(
            f"Вы указали: <b>{amount:,}{oc.values_symbols[user['style']].get(value, f' {value}')}</b>."
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
        user = await rq.SelectUser.load(message.from_user.id)
        premium_user = await user.premium()
        profile = Profile.get(message.from_user.id)
        await checker_num(message.text, profile.value, premium_user)
        profile.choise = "+" + message.text
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
        user = await rq.SelectUser.load(message.from_user.id)
        premium_user = await user.premium()
        profile = Profile.get(message.from_user.id)
        await checker_num(message.text, profile.value, premium_user)
        profile.choise = "-" + message.text
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


# balance input crypto
@router.message(Balance.input_crypto)
async def balance_input_crypto(message: Message, state: FSMContext):
    user_value = message.text.upper()
    value = await checker_value(user_value)

    profile = Profile.get(message.from_user.id)
    choise = profile.choise
    log.debug(f"choise: {choise}")
    answer_, text = await choise_value(value)
    profile.value = value

    if choise == "change":
        log.debug("Change value")
        await state.set_state(Balance.add)
        await message.answer(
            text + "\nУкажите ваши накопления в сообщения(дробные числа указываются точкой):"
        )

    elif choise == "deprive":
        log.debug("Deprive value")
        await state.set_state(Balance.deprive)
        await message.answer(
            text + "\nУкажите ваши траты в сообщения(дробные числа указываются точкой):"
        )

    elif choise == "edit":
        text = await os.default_value_edit(value, message.from_user.id)
        await message.answer(text)


@router.message(Balance.assets_end)
async def add_transaction(message: Message, state: FSMContext):
    try:
        profile = Profile.get(message.from_user.id)
        assets = profile.choise
        description = str(message.text)
        transaction = await rq.Transactions.load(message.from_user.id)

        await transaction.add(profile.value, assets, description)
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
        profile = Profile.get(message.from_user.id)
        user_obj = await rq.SelectUser.load(message.from_user.id)
        premium_user = await user_obj.premium()
        user = user_obj.user
        await checker_num(message.text, user["value"], premium_user)
        profile.choise = float(message.text)
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
        profile = Profile.get(message.from_user.id)
        num_id = int(message.text)
        amount = profile.choise
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
        await transaction.delete(num_id, message.from_user.id)
        await message.answer("Транзакция успешно удалена!")
        log.debug(f"Delete transaction {message.from_user.id}")
    except BadUserIdError as ex:
        await message.answer(f"{ex}")
    finally:
        await state.clear()
