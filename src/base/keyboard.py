from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Баланс💰", callback_data="main_balance")
        ],
        [
            InlineKeyboardButton(text="Конвертация🏪", callback_data="main_conversion"),
            InlineKeyboardButton(text="Список валют📖", callback_data="main_listCurrency")
        ],
        [
            InlineKeyboardButton(text="Активы💸", callback_data="main_assets"),
            InlineKeyboardButton(text="Транзакции📔", callback_data="main_transactions"),
        ],
        [
            InlineKeyboardButton(text="Профиль👤", callback_data="main_profile")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Главное меню🏠", callback_data="menu")
    ]
])

back_to_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Назад⬅️", callback_data="menu")
    ]
])
