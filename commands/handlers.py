from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject
from time import sleep

from operations.transactions import ListTransactions
from operations.conversion import Convert_Balance
from loggers.logs import log
from database.online_config import Profile

# все функции, которые начинаются с rq или kb, берутся с этих файлов
import commands.keyboards as kb
import database.requests as rq
import database.online_config as oc

router = Router()


# стартовая команда
@router.message(CommandStart())
async def start_bot(message: Message):
    await message.delete()
    await rq.SelectUser.load(message.from_user.id)
    oc.msg[message.from_user.id] = await message.answer(
        "Здраствуйте!"
        "\nЗдесь вы можете конвертировать криптовалюты, звезды и обычные деньги,"
        "\nВы также можете учитывать активы и расходы в различных валютах — итоговые значения будут автоматически пересчитаны в единую валюту!"
        "\n\nДля начала работы, нажмите кнопку ниже👇",
        reply_markup=kb.main,
    )
    sleep(2)
    await message.answer(
        "Также ты можешь подписаться на наш канал по Копейке и другим ботам, там выходят обновления и анонсы.",
        reply_markup=kb.sub_channel,
    )


@router.message(Command("info"))
async def info(message: Message):
    await message.answer(oc.terms_of_service)


@router.message(Command("give_premium"))
async def give_premium(message: Message, command: CommandObject):
    if message.from_user.id == 1429466470:
        user_id = int(command.args)
        log.debug(f"Give premium to {user_id}")
        await rq.Edit.premium_extend(user_id)
        await message.answer(f"Вы дали премиум на месяц пользователю: <b><code>{user_id}</code></b>")


# Обработка кнопок
# кнопка назад
@router.message(F.text == "Назад⬅️")
async def back_button(message: Message):
    await message.answer("Вы перешли в главное меню👇", reply_markup=kb.main)


# проверка баланса
@router.message(F.text == "Баланс💲")
async def balance_check(message: Message):
    user_id = message.from_user.id
    con = await Convert_Balance.con_balance(user_id, oc.rates)
    user_obj = await rq.SelectUser.load(user_id)
    user = user_obj.user
    value = user.get("value")
    style = user.get("style")
    value = oc.values_symbols[style].get(value, f" {value[:3]}")
    log.debug(f"Check balance {message.from_user.id}")
    await message.answer(
        f"Ваш баланс активов – <b>{con.balance}{value}</b>\n"
        f"Добавить актив можно, нажав на кнопку в клавиатуре бота."
    )


@router.message(F.text == "Конвертация🏪")
async def conversion(message: Message):
    user_id = message.from_user.id
    user_obj = await rq.SelectUser.load(user_id)
    premium = await user_obj.premium()
    profile = Profile.get(user_id)
    profile.text = "Укажите валюту, в которую хотите конвертировать:"
    profile.con_value = None
    await message.answer(
        "Укажите валюту, в которую хотите конвертировать:",
        reply_markup=kb.con.popular_values(premium, "con"),
    )


# Добавление клавиатуры активов
@router.message(F.text == "Активы💸")
async def assets_keyboard(message: Message):
    await message.answer(
        'Вы перешли в "Операции с активами"' "\nВыберите нужное вам действие:",
        reply_markup=kb.assets,
    )


@router.message(F.text == "Список валют📖")
async def list_region_values(message: Message):
    await message.answer(
        "<b>Выберите регион страны</b>,\nкод валюты которой вы желаете посмотреть.\n"
        "Или вы можете выбрать <b>Популярные валюты</b> и <b>Криптовалюты</b>.",
        reply_markup=kb.clbk.regions(),
    )


# add assets
@router.message(F.text == "Добавить активы💸")
async def add_assets(message: Message):
    user_obj = await rq.SelectUser.load(message.from_user.id)
    premium = await user_obj.premium()
    profile = Profile.get(message.from_user.id)
    profile.choise = "change"
    profile.text = "Укажите <b>валюту</b>:"
    await message.answer(
        "Укажите <b>валюту</b>:",
        reply_markup=kb.con.popular_values(premium, convertation=False),
    )


# deprive assets
@router.message(F.text == "Указать траты📉")
async def deprive_assets(message: Message):
    user_obj = await rq.SelectUser.load(message.from_user.id)
    premium = await user_obj.premium()
    profile = Profile.get(message.from_user.id)
    profile.choise = "deprive"
    profile.text = "Укажите <b>валюту</b>:"
    await message.answer(
        "Укажите <b>валюту</b>:",
        reply_markup=kb.con.popular_values(premium, convertation=False),
    )


#
@router.message(F.text == "Транзакции🔁")
async def transactions_keyboard(message: Message):
    await message.answer(
        'Вы перешли в "Операции с транзакциями"' "\nВыберите нужное вам действие:",
        reply_markup=kb.trasnactions,
    )


# обработка запросов в базу данных для получения красивой картинки транзакций
@router.message(F.text == "История транзакций📋")
async def check_history_transactions(message: Message):
    list_transactions = await ListTransactions.load(message.from_user.id)
    transactions = list_transactions.get()
    if list_transactions.pages() > 1:
        await message.answer(
            transactions,
            reply_markup=kb.clbk.transactions(message.from_user.id),
        )
    else:
        await message.answer(transactions)
    log.debug(f"Check history transactions {message.from_user.id}")


@router.message(F.text == "Изменить транзакцию📝")
async def edit_transaction(message: Message):
    await message.answer("Выберите что сделать с транзакцией:", reply_markup=kb.set.edit_transaction())


@router.message(F.text == "Настройки⚙️")
async def settings(message: Message):
    user_obj = await rq.SelectUser.load(message.from_user.id)
    premium_user = await user_obj.premium()
    await message.answer(
        "Выбери параметр который хочешь изменить.", reply_markup=kb.set.settings(premium_user)
    )
