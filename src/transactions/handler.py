from aiogram.types import CallbackQuery

from transactions import transaction_req, list_transactions

from middlewares.logger import log
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
