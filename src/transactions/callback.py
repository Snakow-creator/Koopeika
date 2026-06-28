from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from config import profile
from core.exceptions import PageError

from keyboards import trx
from states import transaction_state
from middlewares.logger import log
from transactions.handler import transactions_handler
from transactions import Transactions


router = Router()


# paginator transactions
@router.callback_query(F.data.startswith("transaction_"))
async def check_list_transactions(callback: CallbackQuery):
    try:
        await callback.answer("")
        user_id = callback.from_user.id
        prof = profile.get(user_id)
        list_transactions = prof.transactions
        page = prof.transactions_page
        action = callback.data.split("_")[-1]

        if action == "left":
            page -= 1

        elif action == "page":  # добавляем кнопку страницы и делаем ее некликабельной
            return

        elif action == "right":
            page += 1

        transactions = await list_transactions.page(page) # get page transactions
        prof.transactions_page = page # set page to profile

        await callback.message.edit_text(
            transactions,
            reply_markup=trx.transactions_paginator(user_id, pages=True),
        )
        log.debug(f"Check history transactions {user_id}, page: {page}")

    except PageError:
        log.debug(f"except PageError by {user_id}")


@router.callback_query(F.data == "edit_transactions")
async def input_transaction(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    prof = profile.get(user_id)
    transactions = prof.transactions
    buttons_trs = await transactions.load_edit_kb()
    # set page 1
    prof.trs_edit_page = 1
    page = 1

    await callback.message.edit_text(
        "Выберите транзакцию:",
        reply_markup=trx.input_transaction(buttons_trs, page),
    )

# choise changes transaction
@router.callback_query(F.data.startswith("edit_transaction_"))
async def edit_transaction(callback: CallbackQuery):
    await callback.answer()
    action = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    prof = profile.get(user_id)
    page = prof.trs_edit_page

    if action == "left":
            page -= 1

    elif action == "page":  # добавляем кнопку страницы и делаем ее некликабельной
        return

    elif action == "right":
        page += 1

    # if data ends an id
    else:
        tr_id = action # get id transaction
        transaction = await Transactions.get_to_id(user_id, tr_id)
        text = (f"<b>📃Транзакция {transaction['id']}:</b>\n" \
                f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                f"💸Сумма: <b>{transaction['amount']}</b>\n" \
                f"Валюта: <b>{transaction['value']}</b>\n" \
                f"Дата: <b>{transaction['time']}</b>\n")

        if transaction["description"]:
            text += f"Коментарий: <b>{transaction['description']}</b>\n"

        await callback.message.edit_text(
            text,
            reply_markup=trx.edit_transaction(tr_id),
        )
        return # stop function cause we need to edit transaction

    # actions with paginator
    transactions_obj = prof.transactions
    buttons_trs = await transactions_obj.edit_page(page)
    prof.trs_edit_page = page

    await callback.message.edit_text(
        "Выберите транзакцию:",
        reply_markup=trx.input_transaction(buttons_trs, page),
    )


@router.callback_query(F.data.startswith("edit_"))
async def edit_transaction(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[-1]
    await callback.answer("")

    if action == "assets":
        await callback.message.edit_text(
            "Напишите актуальную сумму своих активов/убытков:"
        )
        await state.set_state(transaction_state.edit)
    elif action == "delete":
        await callback.message.edit_text(
            "Напиши айди транзакции, которую хочешь удалить"
        )
        await state.set_state(transaction_state.delete)


@router.callback_query(F.data == "back_to_transactions")
async def back_to_transactions(callback: CallbackQuery):
    await callback.answer()

    await transactions_handler(callback)


