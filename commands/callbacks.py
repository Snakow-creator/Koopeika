from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import commands.handlers as h
import commands.keyboards as kb
import database.online_config as oc
import database.requests as rq
import operations.settings as os
from database.errors_config import ManyTransactionsError
from operations.add_database import check_list_values
from operations.conversion import convert_currency
from operations.transactions import get_history_transactions


router = Router()


@router.callback_query(F.data.startswith("info_"))
async def info(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]  # Извлекаем последние буквы callback_data
    await callback.message.edit_text(text=oc.currency_dict[action], reply_markup=kb.back_regions)


# выполняем функцию отвечающую на кнопку "Без комментариев"
@router.callback_query(F.data == "without_comment")
async def clbk_add_transaction(callback: CallbackQuery, state: FSMContext):
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
async def back_reg(callback: CallbackQuery):
    await callback.answer("Вы вернулись обратно.)")
    await callback.message.edit_text(
        "<b>Выберите регион страны</b>,\nкод валюты которой вы желаете посмотреть.",
        reply_markup=kb.regions(),
    )


# обработка кнопок с сообщения транзакций
# все условия связанные с return, пропускают функцию
@router.callback_query(F.data.startswith("clbk_transaction_"))
async def callback_transactions(callback: CallbackQuery):
    list_transactions = await get_history_transactions(
        callback.from_user.id
    )  # берем функцию с файла transactions
    page = oc.data_page.get(callback.from_user.id, 0)
    user_transactions = oc.data_user_transactions.get(callback.from_user.id)
    action = callback.data.split("_")[2]

    await callback.answer("")

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


@router.callback_query(F.data.startswith("add_value_"))
async def clbk_values(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[-1]  # Извлекаем последние 3 буквы callback_data
    choise = oc.user_choise.get(callback.from_user.id)

    value, answer_, text = await check_list_values(action)
    oc.data_value[callback.from_user.id] = value
    await callback.answer(answer_)

    if choise == "change":
        await state.set_state(h.Balance.change)
        await callback.message.edit_text(
            text + "\nУкажите ваши накопления в сообщения(дробные числа указываются точкой):"
        )

    elif choise == "deprive":
        await state.set_state(h.Balance.deprive)
        await callback.message.edit_text(
            text + "\nУкажите ваши траты в сообщения(дробные числа указываются точкой):"
        )
        
    elif choise == "edit":
        text = await os.clbk_value_edit(action, callback.from_user.id)
        await callback.message.edit_text(text)


@router.callback_query(F.data.startswith("clbk_otherlist_"))
async def check_fulllist(callback: CallbackQuery):
    await callback.answer("")

    action = callback.data.split("_")[-1]
    await callback.message.edit_text("Укажите валюту:", reply_markup=kb.clbk.full_list(action))


# сохраняем первую валюту(конвертация)
@router.callback_query(F.data.startswith("con_value_"))
async def input_number(callback: CallbackQuery, state: FSMContext):
    await state.set_state(h.Conversion.input_number)  # Устанавливаем состояние

    action = callback.data.split("_")[-1]  # Извлекаем последние буквы callback_data
    value, answer_, text = await check_list_values(action)
    oc.first_con_value[callback.from_user.id] = value  # сохраняем первую валюту
    await callback.answer(answer_)
    await callback.message.edit_text(f"{text}\nУкажите количество валюты, которое вы хотите конвертировать:")


# получаем вторую валюту и получаем результат конвертации
@router.callback_query(F.data.startswith("endcon_value_"))
async def output_number(callback: CallbackQuery):
    await callback.answer("")
    # получаем необходимые данные
    user_id = callback.from_user.id
    value = callback.data.split("_")[-1]  # Извлекаем последние буквы callback_data
    amount = oc.input_value.get(user_id)
    style = await rq.get_style(user_id)
    # получаем заданые и итоговые значения валют и их количество
    f_con_value = oc.first_con_value.get(user_id)
    converted_amount = await convert_currency(amount, f_con_value, value, oc.rates)
    in_symbol = oc.values_symbols[style][f_con_value]
    out_symbol = oc.values_symbols[style][value]

    await callback.message.edit_text(
        f"Конвертация: {amount} <b>{in_symbol}</b> = {converted_amount} <b>{out_symbol}</b>"
    )


@router.callback_query(F.data.startswith("clbk_edit_"))
async def clbk_check_settings(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]  # Извлекаем последние буквы callback_data
    if action == "timezone":
        await os.change_time_zone(callback)

    elif action == "value":
        oc.user_choise[callback.from_user.id] = "edit"
        await callback.message.edit_text(
            "Выберите валюту по умолчанию:", reply_markup=kb.clbk.classic_values()
        )

    elif action == "style":
        await os.clbk_style(callback)

    elif action == "info":
        await os.clbk_info(callback)


@router.callback_query(F.data.startswith("time_zone_"))
async def clbk_timezone_input(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]  # Извлекаем последние буквы callback_data
    user_id = callback.from_user.id
    text = await os.clbk_time_zone_edit(action, user_id)

    await callback.answer("Успешно✅")
    await callback.message.edit_text(text)


@router.callback_query(F.data.startswith("style_"))
async def change_style(callback: CallbackQuery):
    await callback.answer("")
    action = callback.data.split("_")[-1]  # Извлекаем последние буквы callback_data
    user_id = callback.from_user.id

    if action == "symbols":
        await rq.style_edit("symbols", user_id)
        await callback.message.edit_text("Вы сменили стиль на <b>Символы</b>")

    elif action == "codename":
        await rq.style_edit("codename", user_id)
        await callback.message.edit_text("Вы сменили стиль на <b>Названия</b>")


@router.callback_query(F.data.startswith("edit_"))
async def edit_transaction(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[-1]
    await callback.answer("")

    if action == "assets":
        await callback.message.edit_text("Напишите актуальную сумму своих активов/убытков:")
        await state.set_state(h.Transaction.edit)
    elif action == "delete":
        await callback.message.edit_text("Напиши айди транзакции, которую хочешь удалить")
        await state.set_state(h.Transaction.delete)
