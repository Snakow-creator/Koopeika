from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart

from database.errors_config import BadMessageText, BadUserIdError, ManyTransactionsError
from database.errors_config import BigNumError
from operations.transactions import get_history_transactions
from operations.conversion import con_balance
from commands.functions import checker_num

# все функции, которые начинаются с rq или kb, берутся с этих файлов
import commands.keyboards as kb
import database.requests as rq
import database.online_config as oc
import operations.settings as os

# роутер и личные переменные юзера
router = Router()


# импорты фсм контекста
class Balance(StatesGroup):
    change = State()
    change_end = State()
    deprive = State()
    deprive_end = State()


class Transaction(StatesGroup):
    edit = State()
    edit_end = State()
    delete = State()


class Conversion(StatesGroup):
    input_number = State()


# стартовая команда
@router.message(CommandStart())
async def start(message: Message):
    await message.delete()
    await rq.add_user(message.from_user.id)
    oc.msg[message.from_user.id] = await message.answer(
        "Привет, будущий экономист, ты по адресу - я помогу тебе с расчетами😃", reply_markup=kb.main
    )


# Обработка кнопок
# кнопка назад
@router.message(F.text == "Назад⬅️")
async def back_button(message: Message):
    await message.answer("Вы перешли в главное меню👇", reply_markup=kb.main)


# проверка баланса
@router.message(F.text == "Баланс💲")
async def check_balance(message: Message):
    user_id = message.from_user.id
    amount = await con_balance(user_id, oc.rates)
    value = await rq.get_value(user_id)
    style = await rq.get_style(user_id)
    value = oc.values_symbols[style][value]
    await message.answer(
        f"Ваш баланс активов = <b>{amount}{value}</b>\n"
        f"Добавить актив можно, нажав на кнопку в клавиатуре бота."
    )


@router.message(F.text == "Конвертация🏪")
async def input_numbers(message: Message, state: FSMContext):
    oc.first_con_value[message.from_user.id] = None
    await message.answer(
        "Укажите валюту, в которую хотите конвертировать:",
        reply_markup=kb.clbk.popular_values("con"),
    )


@router.message(Conversion.input_number)
async def input_values(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        oc.input_value[user_id] = float(message.text)
        value = oc.first_con_value[user_id]
        style = await rq.get_style(user_id)

        await state.clear()
        await message.answer(
            f"Вы указали: {message.text} {oc.values_symbols[style][value]}."
            f"\nВыберите валюту из которой будет перевод⬇️",
            reply_markup=kb.clbk.popular_values("endcon"),
        )
    except ValueError:
        await message.answer(
            "Ошибка в получении сообщения, скорее всего вы ввели неприемлемый тип сообщения."
        )
        await state.clear()


# Добавление клавиатуры активов
@router.message(F.text == "Активы💸")
async def assets_keyboard(message: Message):
    await message.answer(
        'Вы перешли в "Операции с активами"' "\nВыберите нужное вам действие:",
        reply_markup=kb.assets,
    )


@router.message(F.text == "Список валют📖")
async def currency_list(message: Message):
    await message.answer(
        "<b>Выберите регион страны</b>,\nкод валюты которой вы желаете посмотреть.\n"
        "Или вы можете выбрать <b>Популярные валюты</b> и <b>Криптовалюты</b>.",
        reply_markup=kb.regions(),
    )


# добавление баланса
@router.message(F.text == "Добавить активы💸")
async def add_assets(message: Message):
    oc.user_choise[message.from_user.id] = "change"
    await message.answer(
        "Укажите <b>валюту</b>:",
        reply_markup=kb.clbk.popular_values(convertation=False),
    )


@router.message(Balance.change)
async def add_assets_con(message: Message, state: FSMContext):
    try:
        value = oc.data_value.get(message.from_user.id, 0)
        await checker_num(message.text, value)
        oc.user_choise[message.from_user.id] = "+" + message.text
        await state.set_state(Balance.change_end)
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


@router.message(Balance.change_end)
async def add_assets_end(message: Message, state: FSMContext):
    try:
        value = oc.data_value.get(message.from_user.id, 0)
        assets = oc.user_choise.get(message.from_user.id, 0)
        description = str(message.text)
        await rq.Transactions.add(value, message.from_user.id, assets, description)
        await message.answer("Функция произведена успешно✅")
    except ManyTransactionsError as ex:
        await message.answer(f"{ex}")
    except AssertionError:
        await message.answer("Ошибка, вы ввели слишком много символов.")
    finally:
        await state.clear()


# списание трат
@router.message(F.text == "Указать траты📉")
async def delete_assets(message: Message):
    oc.user_choise[message.from_user.id] = "deprive"
    await message.answer(
        "Укажите <b>валюту</b>:",
        reply_markup=kb.clbk.popular_values(convertation=False),
    )


@router.message(Balance.deprive)
async def delete_assets_con(message: Message, state: FSMContext):
    try:
        value = oc.data_value.get(message.from_user.id, 0)
        await checker_num(message.text, value)
        oc.user_choise[message.from_user.id] = "-" + message.text
        await state.set_state(Balance.deprive_end)
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


@router.message(Balance.deprive_end)
async def delete_assets_end(message: Message, state: FSMContext):
    try:
        value = oc.data_value.get(message.from_user.id, 0)
        assets = oc.user_choise.get(message.from_user.id, 0)
        description = str(message.text)
        await rq.Transactions.add(value, message.from_user.id, assets, description)
        await message.answer("Функция произведена успешно✅")
    except AssertionError:
        await message.answer("Ошибка, вы ввели слишком много символов")
    except ManyTransactionsError as ex:
        await message.answer(f"{ex}")
    finally:
        await state.clear()


# Добавление клавиатуры транзакции
@router.message(F.text == "Транзакции🔁")
async def transactions(message: Message):
    await message.answer(
        'Вы перешли в "Операции с транзакциями"' "\nВыберите нужное вам действие:",
        reply_markup=kb.trasnactions,
    )


# обработка запросов в базу данных для получения красивой картинки транзакций
@router.message(F.text == "История транзакций📋")
async def check_history_transactions(message: Message):
    oc.data_page[message.from_user.id] = 1
    list_transactions = await get_history_transactions(message.from_user.id)
    if len(list_transactions) > 1:
        await message.answer(
            list_transactions[0],
            reply_markup=kb.clbk.transactions(message.from_user.id),
        )
    else:
        await message.answer(list_transactions[0])


@router.message(F.text == "Изменить транзакцию📝")
async def edit_transaction(message: Message):
    await message.answer("Выберите что сделать с транзакцией:", reply_markup=kb.clbk.change_transaction())


@router.message(Transaction.edit)
async def con_transaction(message: Message, state: FSMContext):
    try:
        value = await rq.get_value(message.from_user.id)
        await checker_num(message.text, value)
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
async def final_transaction(message: Message, state: FSMContext):
    try:
        num_id = int(message.text)
        amount = oc.user_choise.get(message.from_user.id)
        await rq.Transactions.edit(value=amount, tg_id=message.from_user.id, num_id=num_id)
        await message.answer("Транзакция успешно изменена!")
    except BadUserIdError as ex:
        await message.answer(f"{ex}")
    finally:
        await state.clear()


@router.message(Transaction.delete)
async def transaction_delete(message: Message, state: FSMContext):
    try:
        num_id = int(message.text)
        await state.clear()
        await rq.Transactions.delete(tg_id=message.from_user.id, num_id=num_id)
        await message.answer("Транзакция успешно удалена!")
    except BadUserIdError as ex:
        await message.answer(f"{ex}")
    finally:
        await state.clear()


@router.message(F.text == "Настройки⚙️")
async def check_settings(message: Message):
    text = await os.text_settings()
    await message.answer(text=text, reply_markup=kb.clbk.settings())
