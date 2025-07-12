from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from commands.states import Conversion, Transaction, Balance
from database.errors_config import ManyTransactionsError
from operations.choise_value import choise_value
from operations.conversion import convert_currency, convert_num
from operations.transactions import get_history_transactions
from loggers.logs import log

import commands.keyboards as kb
import database.online_config as oc
import database.requests as rq
import operations.settings as os

router = Router()


@router.callback_query(F.data.startswith("info_"))
async def info_region_value(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]  # Извлекаем последние буквы callback_data
    await callback.message.edit_text(text=oc.currency_dict[action],
                                     reply_markup=kb.clbk.back_regions(),
                                     disable_web_page_preview=True)


# выполняем функцию отвечающую на кнопку "Без комментариев"
@router.callback_query(F.data == "without_comment")
async def add_transaction_without_comment(callback: CallbackQuery, state: FSMContext):
    try:
        value = oc.data_value.get(callback.from_user.id, 0)
        assets = oc.user_choise.get(callback.from_user.id, 0)
        await rq.Transactions.add(value, callback.from_user.id, assets, description="")
        await callback.message.edit_text("Функция произведена успешно.")
    except ManyTransactionsError as ex:
        await callback.message.edit_text(str(ex))
    finally:
        await state.clear()


@router.callback_query(F.data == "back_reg")
async def back_region(callback: CallbackQuery):
    await callback.answer("Вы вернулись обратно.)")
    await callback.message.edit_text(
        "<b>Выберите регион страны</b>,\nкод валюты которой вы желаете посмотреть.",
        reply_markup=kb.clbk.regions(),
    )


# обработка кнопок с сообщения транзакций
# все условия связанные с return, пропускают функцию
@router.callback_query(F.data.startswith("transaction_"))
async def check_list_transactions(callback: CallbackQuery):
    await callback.answer("")

    list_transactions = await get_history_transactions(
        callback.from_user.id
    )  # берем функцию с файла transactions
    page = oc.data_page.get(callback.from_user.id, 0)
    user_transactions = oc.data_user_transactions.get(callback.from_user.id)
    action = callback.data.split("_")[-1]

    if action == "left":
        if page > 1:
            page -= 1
        else:
            return

    elif action == "page":  # добавляем кнопку страницы и делаем ее некликабельной
        return

    elif action == "right":
        if page < (len(user_transactions)):
            page += 1
        else:
            return

    oc.data_page[callback.from_user.id] = page

    await callback.message.edit_text(
        list_transactions[page - 1],
        reply_markup=kb.clbk.transactions(callback.from_user.id),
    )
    log.debug(f"Check history transactions {callback.from_user.id}, page: {page}")


# input popular and full list values, for classic values list smaller
@router.callback_query(F.data.startswith("add_value_"))
async def add_transaction(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[-1]  # Извлекаем последние 3 буквы callback_data
    choise = oc.user_choise.get(callback.from_user.id)

    value, answer_, text = await choise_value(action)
    oc.data_value[callback.from_user.id] = value
    await callback.answer(answer_)

    if choise == "change":
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
        text = await os.default_value_edit(action, callback.from_user.id)
        await callback.message.edit_text(text)


@router.callback_query(F.data.startswith("otherlist_value_"))
async def check_fulllist_values(callback: CallbackQuery):
    await callback.answer("")

    action = callback.data.split("_")[-1]
    await callback.message.edit_text("Укажите валюту:", reply_markup=kb.con.full_list_values(action))


@router.callback_query(F.data.startswith("value_back_"))
async def value_back(callback: CallbackQuery):
    action = callback.data.split("_")[-1] # input last parametr in callback_data
    text = oc.user_text.get(callback.from_user.id)
    await callback.message.edit_text(text, reply_markup=kb.con.popular_values(action))




# save first value, input popular and full list values
@router.callback_query(F.data.startswith("con_value_"))
async def con_input_value(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Conversion.input_number)  # install state

    user_id = callback.from_user.id
    style = await rq.Get.style(callback.from_user.id)
    action = callback.data.split("_")[-1]  # input last word in callback_data
    value, answer_, text = await choise_value(action)
    oc.first_con_value[callback.from_user.id] = value  # save first value

    await callback.answer(answer_)
    oc.msg[user_id] = await callback.message.edit_text(
        f"{text}\nУкажите количество валюты, которое вы хотите конвертировать:"
        f"\nИли нажмите на число ниже⬇️",
        reply_markup=kb.con.input_numbers(oc.values_symbols[style][value]),
    )


# get fast input amount value
@router.callback_query(F.data.startswith("con_input_amount_"))
async def con_fast_input_second_value(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")

    user_id = callback.from_user.id
    action = callback.data.split("_")[-1]  # get amount
    value = oc.first_con_value[user_id]
    style = await rq.Get.style(user_id)

    oc.input_value[user_id] = int(action)
    oc.user_text[user_id] = (
        f"Вы указали: <b>{int(action)}{oc.values_symbols[style][value]}</b>."
        f"\nВыберите валюту, в которую требуется конвертировать сумму⬇️"
    )
    if value == "⭐️":
        keyboard = kb.con.stars_popular_values()
    else:
        keyboard = kb.con.popular_values("endcon")

    await state.clear()
    await callback.message.edit_text(
        oc.user_text[user_id],
        reply_markup=keyboard
    )


# input second value and output result
@router.callback_query(F.data.startswith("endcon_value_"))
async def con_output_result(callback: CallbackQuery):
    await callback.answer("")
    # получаем необходимые данные
    user_id = callback.from_user.id
    value = callback.data.split("_")[-1]  # input last word in callback_data
    amount = oc.input_value.get(user_id)
    style = await rq.Get.style(user_id)

    # get two values and convert it
    first_value = oc.first_con_value.get(user_id)
    con_amount = await convert_currency(amount, first_value, value, oc.rates)
    converted_amount = await convert_num(con_amount, value, user_id)
    from_symbol = oc.values_symbols[style][first_value]
    to_symbol = oc.values_symbols[style][value]
    log.debug(f"Conversion {callback.from_user.id}")
    await callback.message.edit_text(
        f"Конвертация: {amount:,}<b>{from_symbol}</b> = {converted_amount}<b>{to_symbol}</b>"
    )


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
    await callback.answer("")
    action = callback.data.split("_")[-1]  # input last word in callback_data
    if action == "timezone":
        await os.change_time_zone(callback)

    elif action == "value":
        oc.user_choise[callback.from_user.id] = "edit"
        await callback.message.edit_text(
            "Выберите валюту по умолчанию:", reply_markup=kb.set.classic_values()
        )

    elif action == "style":
        await os.clbk_style(callback)

    elif action == "info":
        await os.settings_user_info(callback)

    elif action == "nums":
        await callback.message.edit_text(
            "Выберите у каких активов вы хотите изменить кол-во десятичных знаков⬇️",
            reply_markup=kb.set.choise_amount(),
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
        await rq.Edit.style("symbols", user_id)
        await callback.message.edit_text("Вы сменили стиль на <b>Символы</b>")

    elif action == "codename":
        await rq.Edit.style("codename", user_id)
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
