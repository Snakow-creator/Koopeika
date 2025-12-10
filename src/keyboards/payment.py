from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class PaymentKeyboard:
    @staticmethod
    def premium_buttons():
        buttons = [
            [
                InlineKeyboardButton(text="1 месяц", callback_data="pay_premium_stars_30"),
                InlineKeyboardButton(text="3 месяца", callback_data="pay_premium_stars_90"),
            ],
            [
                InlineKeyboardButton(text="6 месяцев", callback_data="pay_premium_stars_180"),
                InlineKeyboardButton(text="12 месяцев", callback_data="pay_premium_stars_365"),
            ],
            [
                InlineKeyboardButton(text="Условия пользования", callback_data="terms_of_service"),
            ],
            [
                InlineKeyboardButton(text="Назад⬅️", callback_data="main_profile"),
            ],
        ]

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def terms_of_services_back():
        builder = InlineKeyboardBuilder()
        builder.button(text="Назад⬅️", callback_data="settings_edit_premium")
        return builder.as_markup()

    @staticmethod
    def premium(amount: int):
        builder = InlineKeyboardBuilder()
        builder.button(text=f"Подписаться на месяц({amount}⭐️)", pay=True)
        return builder.as_markup()
