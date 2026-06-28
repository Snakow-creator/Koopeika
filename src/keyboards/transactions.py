from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import profile


class TransactionsKeyboard:
    @staticmethod
    def transactions_paginator(tg_id=None, pages=False) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(
                    text="Изменить транзакцию✏️", callback_data="edit_transactions"
                )
            ]
        ]

        if pages:
            page = profile.get(tg_id).transactions_page
            buttons.append(
                [
                    InlineKeyboardButton(text="⬅️", callback_data="transaction_left"),
                    InlineKeyboardButton(text=f"{page}", callback_data="transaction_page"),
                    InlineKeyboardButton(text="➡️", callback_data="transaction_right"),
                ]
            )

        buttons.append(
            [
                InlineKeyboardButton(text="Назад⬅️", callback_data="menu"),
            ]
        )

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def input_transaction(buttons_trs, page) -> InlineKeyboardMarkup:
        buttons = []
        for id, tr in buttons_trs:
            buttons.append([InlineKeyboardButton(text=tr, callback_data=f"edit_transaction_{id}")])
        buttons.append(
            [
                InlineKeyboardButton(text="⬅️", callback_data="edit_transaction_left"),
                InlineKeyboardButton(text=f"{page}", callback_data="edit_transaction_page"),
                InlineKeyboardButton(text="➡️", callback_data="edit_transaction_right"),
            ]
        )
        buttons.append([InlineKeyboardButton(text="Назад⬅️", callback_data="back_to_transactions")])
        return InlineKeyboardMarkup(inline_keyboard=buttons)


    @staticmethod
    def edit_transaction(id) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="Изменить сумму✏️", callback_data=f"edit_transaction_assets_{id}"),
                InlineKeyboardButton(text="Удалить транзакцию🗑", callback_data=f"edit_transaction_delete_{id}"),
            ],
            [InlineKeyboardButton(text="Назад⬅️", callback_data="back_to_transactions")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
