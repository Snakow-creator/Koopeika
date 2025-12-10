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
    def edit_transaction() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="Изменить сумму✏️", callback_data="edit_transaction_assets"),
                InlineKeyboardButton(text="Удалить транзакцию🗑", callback_data="edit_transaction_delete"),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
