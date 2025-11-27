from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from commands.states import Con, Transaction, Balance
from commands.payments import payment_stars
from database.errors_config import ManyTransactionsError, PageError
from database.online_config import Profile
from operations.choise_value import choise_value
from operations.conversion import Conversion
from loggers.logs import log

import commands.keyboards as kb
import database.online_config as oc
import database.requests as rq
import operations.settings as os

router = Router()


# info regions
@router.callback_query(F.data.startswith("info_"))
async def info_region_value(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]  # Извлекаем последние буквы callback_data
    await callback.message.edit_text(
        text=oc.currency_dict[action], reply_markup=kb.clbk.back_regions(), disable_web_page_preview=True
    )


@router.callback_query(F.data == "terms_of_service")
async def terms_of_service(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text(oc.terms_of_service, reply_markup=kb.pay.terms_of_services_back())


# back button to choise regions
@router.callback_query(F.data == "back_reg")
async def back_region(callback: CallbackQuery):
    await callback.answer("Вы вернулись обратно.)")
    await callback.message.edit_text(
        "<b>Выберите регион страны</b>,\nкод валюты которой вы желаете посмотреть.",
        reply_markup=kb.clbk.regions(),
    )


# choise changes transaction
@router.callback_query(F.data == "edit_transactions")
async def edit_transaction(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "Выберите действие с транзакцией:", reply_markup=kb.set.edit_transaction()
    )


# paginator transactions
@router.callback_query(F.data.startswith("transaction_"))
async def check_list_transactions(callback: CallbackQuery):
    try:
        await callback.answer("")
        user_id = callback.from_user.id
        profile = oc.Profile.get(user_id)
        list_transactions = profile.transactions
        page = profile.transactions_page
        action = callback.data.split("_")[-1]

        if action == "left":
            page -= 1

        elif action == "page":  # добавляем кнопку страницы и делаем ее некликабельной
            return

        elif action == "right":
            page += 1

        transactions = await list_transactions.page(page)
        profile.transactions_page = page

        await callback.message.edit_text(
            transactions,
            reply_markup=kb.clbk.transactions(user_id),
        )
        log.debug(f"Check history transactions {user_id}, page: {page}")

    except PageError:
        log.debug(f"except PageError by {user_id}")


# input popular and full list values, for classic values list smaller
@router.callback_query(F.data.startswith("add_value_"))
async def add_transaction(callback: CallbackQuery, state: FSMContext):
    value = callback.data.split("_")[-1]  # Извлекаем последние 3 буквы callback_data
    profile = Profile.get(callback.from_user.id)
    choise = profile.choise
    log.debug(f"choise: {choise}")
    answer_, text = await choise_value(value)
    profile.value = value
    await callback.answer(answer_)

    if choise == "change":
        log.debug("Change value")
        await state.set_state(Balance.add)
        await callback.message.edit_text(
            text + "\nУкажите ваши накопления в сообщения(дробные числа указываются точкой):"
        )

    elif choise == "deprive":
        await state.set_state(Balance.deprive)
        await callback.message.edit_text(
            text + "\nУкажите ваши траты в сообщения(дробные числа указываются точкой):"
        )

    elif choise == "edit":
        text = await os.default_value_edit(value, callback.from_user.id)
        await callback.message.edit_text(text)


# add assets or deprive
@router.callback_query(F.data.startswith("add_assets_"))
async def add_assets(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]

    user_obj = await rq.SelectUser.load(callback.from_user.id)
    premium = await user_obj.premium()
    profile = Profile.get(callback.from_user.id)
    profile.choise = action
    profile.text = "Укажите <b>валюту</b>:"
    await callback.message.edit_text(
        "Укажите <b>валюту</b>:",
        reply_markup=kb.con.popular_values(premium, convertation=False),
    )


# выполняем функцию отвечающую на кнопку "Без комментариев"
@router.callback_query(F.data == "without_comment")
async def add_transaction_without_comment(callback: CallbackQuery, state: FSMContext):
    try:
        profile = Profile.get(callback.from_user.id)
        transaction = await rq.Transactions.load(callback.from_user.id)
        await transaction.add(profile.value, profile.choise, "")
        await callback.message.edit_text("Функция произведена успешно.")
    except ManyTransactionsError as ex:
        await callback.message.edit_text(str(ex))
    finally:
        await state.clear()


@router.callback_query(F.data.startswith("otherlist_value_"))
async def check_fulllist_values(callback: CallbackQuery):
    await callback.answer("")

    action = callback.data.split("_")[-1]
    await callback.message.edit_text("Укажите валюту:", reply_markup=kb.con.full_list_values(action))


@router.callback_query(F.data.startswith("cryptolist_value_"))
async def check_fulllist_values(callback: CallbackQuery):
    await callback.answer("")

    user_obj = await rq.SelectUser.load(callback.from_user.id)
    max_coins = user_obj.user.get("crypto_max_coins")

    action = callback.data.split("_")[-1]
    await callback.message.edit_text("Укажите валюту:", reply_markup=kb.con.crypto_values(max_coins, action))


@router.callback_query(F.data.startswith("value_back_"))
async def value_back(callback: CallbackQuery):
    user_obj = await rq.SelectUser.load(callback.from_user.id)
    premium_user = await user_obj.premium()
    action = callback.data.split("_")[-1]  # input last parametr in callback_data
    text = Profile.get(callback.from_user.id).text
    await callback.message.edit_text(text, reply_markup=kb.con.popular_values(premium_user, action))


@router.callback_query(F.data == "con_value_pop_⭐️")
async def stars_input_value(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Con.input_number)  # install state
    await callback.answer("")
    await callback.message.edit_text(
        "Выберите нужное действие для звёзд⭐️" "\nУчтите, что курс зависит от <b>направления обмена</b>",
        reply_markup=kb.con.stars_choise(),
    )


# input cryptovalue
@router.callback_query(F.data.startswith("input_crypto_"))
async def input_crypto(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    action = callback.data.split("_")[-1]
    print(action)

    if action == "add":
        log.debug("Change value")
        await state.set_state(Balance.input_crypto)
    if action in ("con", "endcon"):
        log.debug("Conversion")
        await state.set_state(Con.input_crypto)

    profile = Profile.get(callback.from_user.id)
    action = callback.data.split("_")[-1]
    profile.con_choise = action
    profile.tr_message_id = callback.message.message_id
    await callback.message.edit_text(
        "Введите название криптовалюты:" \
        "\n➖➖➖➖➖" \
        "\nУказывайте название пожалуйста в формате <b>кодового названия</b>(например: BTCUSDT, ETHUSDT)",
        reply_markup=kb.con.back_button(action),
    )


# save first value, input popular and full list values
@router.callback_query(F.data.startswith("con_value_"))
async def con_input_value(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Con.input_number)  # install state
    profile = Profile.get(callback.from_user.id)
    user_id = callback.from_user.id
    user_obj = await rq.SelectUser.load(callback.from_user.id)
    user = user_obj.user
    value = callback.data.split("_")[-1]  # input last word in callback_data
    answer_, text = await choise_value(value)
    profile.con_value = value  # save first value

    await callback.answer(answer_)
    oc.msg[user_id] = await callback.message.edit_text(
        f"{text}\nУкажите количество валюты, которое вы хотите конвертировать:"
        f"\nИли нажмите на число ниже⬇️",
        reply_markup=kb.con.input_numbers(oc.values_symbols[user["style"]].get(value, f' {value}')),
    )


# get fast input amount value
@router.callback_query(F.data.startswith("con_input_amount_"))
async def con_fast_input_second_value(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    user_id = callback.from_user.id
    profile = Profile.get(user_id)
    action = callback.data.split("_")[-1]  # get amount
    value = profile.con_value
    user_obj = await rq.SelectUser.load(user_id)
    user = user_obj.user
    premium_user = await user_obj.premium()
    profile.amount = int(action)
    profile.text = (
        f"Вы указали: <b>{int(action)}{oc.values_symbols[user['style']].get(value, f' {value}')}</b>."
        f"\nВыберите валюту, в которую требуется конвертировать сумму⬇️"
    )
    if value[0:2] == "⭐️":
        keyboard = kb.con.stars_popular_values(premium_user)
    else:
        keyboard = kb.con.popular_values(premium_user, "endcon")

    await state.clear()
    await callback.message.edit_text(profile.text, reply_markup=keyboard)


# input second value and output result
@router.callback_query(F.data.startswith("endcon_value_"))
async def con_output_result(callback: CallbackQuery):
    await callback.answer("")
    # получаем необходимые данные
    user_id = callback.from_user.id
    profile = Profile.get(user_id)
    value = callback.data.split("_")[-1]  # input last word in callback_data
    amount = profile.amount
    user_obj = await rq.SelectUser.load(user_id)
    user = user_obj.user

    # get two values and convert it
    first_value = profile.con_value
    result = await Conversion.conversion(user_id, first_value, value, amount, oc.rates)
    from_symbol = oc.values_symbols[user["style"]].get(first_value, f" {first_value}")
    to_symbol = oc.values_symbols[user["style"]].get(value, f" {value}")
    log.debug(f"Conversion {callback.from_user.id}")
    await callback.message.edit_text(result.text(from_symbol, to_symbol))


@router.callback_query(F.data.startswith("edit_"))
async def edit_transaction(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[-1]
    await callback.answer("")

    if action == "assets":
        await callback.message.edit_text("Напишите актуальную сумму своих активов/убытков:")
        await state.set_state(Transaction.edit)
    elif action == "delete":
        await callback.message.edit_text("Напиши айди транзакции, которую хочешь удалить")
        await state.set_state(Transaction.delete)


@router.callback_query(F.data.startswith("settings_edit_"))
async def settings_action(callback: CallbackQuery):
    user_obj = await rq.SelectUser.load(callback.from_user.id)
    premium_user = await user_obj.premium()
    await callback.answer("")
    action = callback.data.split("_")[-1]  # input last word in callback_data
    if action == "timezone":
        await os.change_time_zone(callback)

    elif action == "value":
        Profile.get(callback.from_user.id).choise = "edit"
        if premium_user:
            keyboard = kb.con.popular_values(premium_user)
        else:
            keyboard = kb.set.classic_values()
        await callback.message.edit_text("Выберите валюту по умолчанию:", reply_markup=keyboard)

    elif action == "style":
        await os.clbk_style(callback)

    elif action == "info":
        text = await os.settings_user_info(premium_user, callback.from_user.id)
        await callback.message.edit_text(text, disable_web_page_preview=True)

    elif action == "nums":
        await callback.message.edit_text(
            "Выберите у каких активов вы хотите изменить кол-во десятичных знаков⬇️",
            reply_markup=kb.set.choise_amount(),
        )

    elif action == "cryptomaxcoins":
        await callback.message.edit_text(
            "Выберите размер списка криптовалют⬇️",
            reply_markup=kb.set.crypto_max_coins(),
        )

    elif action == "premium":
        await callback.message.edit_text(
            "Хотите получить больше возможностей и валют?\n\n"
            "Купите <b>Koopeika Premium</b> и откройте возможности:\n"
            "1. Выбор до 48 криптовалют\n"
            "2. Выбор <b>криптовалют</b> и <b>Telegram Stars</b> по умолчанию\n"
            "3. Конвертация из звезд в криптовалюту\n"
            "4. Лимит до 300 транзакций(по умолчанию 50)\n"
            "5. Увеличен лимит на сумму валют в 1000 раз",
            reply_markup=kb.pay.premium_buttons(),
        )


@router.callback_query(F.data.startswith("time_zone_"))
async def settings_change_time_zone(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]  # input last word in callback_data
    user_id = callback.from_user.id
    text = await os.time_zone_edit(action, user_id)
    await callback.answer("Успешно✅")
    await callback.message.edit_text(text)
    log.debug(f"User {user_id} change time zone to {action}")


@router.callback_query(F.data.startswith("style_"))
async def settings_change_style(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]  # input last word in callback_data
    user_id = callback.from_user.id

    if action == "symbols":
        await rq.Edit.style(user_id, "symbols")
        await callback.message.edit_text("Вы сменили стиль на <b>Символы</b>")

    elif action == "codename":
        await rq.Edit.style(user_id, "codename")
        await callback.message.edit_text("Вы сменили стиль на <b>Названия</b>")
    log.debug(f"""User {user_id} change style to {action}""")


@router.callback_query(F.data.startswith("amount_edit_"))
async def settings_choise_amount(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]
    if action == "fiat":
        await callback.message.edit_text(
            "Укажите количество цифр после точки(фиат):", reply_markup=kb.set.choise_fiat_amount()
        )

    elif action == "crypto":
        await callback.message.edit_text(
            "Укажите количество цифр после точки(криптовалюта):", reply_markup=kb.set.choise_crypto_amount()
        )


@router.callback_query(F.data.startswith("fiat_amount_"))
async def settings_set_fiat_amount(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]
    await os.fiat_amount_edit(int(action), callback.from_user.id)
    await callback.message.edit_text(f"Вы изменили количество цифр после запятой(фиат) на <b>{action}</b>")


@router.callback_query(F.data.startswith("crypto_amount_"))
async def settings_set_crypto_amount(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]
    await os.crypto_amount_edit(int(action), callback.from_user.id)
    await callback.message.edit_text(
        f"Вы изменили количество цифр после запятой(криптовалюта) на <b>{action}</b>"
    )


# edit crypto max coins
@router.callback_query(F.data.startswith("crypto_max_"))
async def settings_set_cryptomaxcoins(callback: CallbackQuery):
    await callback.answer("")
    action = int(callback.data.split("_")[-1])
    text = await os.crypto_max_coins_edit(action, callback.from_user.id)
    await callback.message.edit_text(text)


@router.callback_query(F.data.startswith("pay_premium_stars_"))
async def pay_premium_month(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-2]

    if action == "stars":
        days = callback.data.split("_")[-1]
        await payment_stars(callback, int(days))
