from aiogram.types import CallbackQuery

from transactions import transaction_req, list_transactions
from config import profile

from tasks.logger import log
from keyboards import trx, main_menu


async def transactions_handler(callback: CallbackQuery):

    # get transactions
    list_tx = await list_transactions.load(callback.from_user.id)
    tx = list_tx.get()

    if list_tx.pages() > 1:
        await callback.message.edit_text(
            tx,
            reply_markup=trx.transactions_paginator(callback.from_user.id, pages=True),
        )
    # elif pages does not exist
    elif list_tx.pages() == -1:
        await callback.message.edit_text(
            "У вас нет активов.\n" "Добавьте активы, чтобы увидеть историю транзакций",
            reply_markup=main_menu,
        )
    # if tx is lower than 10
    else:
        await callback.message.edit_text(tx, reply_markup=trx.transactions_paginator(callback, pages=False))

    log.debug(f"Check history transactions {callback.from_user.id}")


async def edit_transactions_handler(callback: CallbackQuery):
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
