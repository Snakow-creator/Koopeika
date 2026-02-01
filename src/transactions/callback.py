from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from config import profile
from core.exceptions import PageError

from keyboards import trx
from states import transaction_state
from middlewares.logger import log


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

        transactions = await list_transactions.page(page)
        prof.transactions_page = page

        await callback.message.edit_text(
            transactions,
            reply_markup=trx.transactions_paginator(user_id, pages=True),
        )
        log.debug(f"Check history transactions {user_id}, page: {page}")

    except PageError:
        log.debug(f"except PageError by {user_id}")


# choise changes transaction
@router.callback_query(F.data == "edit_transactions")
async def edit_transaction(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "Выберите действие с транзакцией:", reply_markup=trx.edit_transaction()
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
