from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# regions keyboard which under message
@staticmethod
def info_regions() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🌍 Европа", callback_data="info_europe"),
            InlineKeyboardButton(text="🌎 Америка", callback_data="info_america"),
            InlineKeyboardButton(text="🌏Азия", callback_data="info_asia"),
        ],
        [
            InlineKeyboardButton(
                text="🌍 Африка и Ближний Восток", callback_data="info_africa"
            ),
            InlineKeyboardButton(text="🌊 Океания", callback_data="info_oceania"),
        ],
        [
            InlineKeyboardButton(
                text="💱 Популярные валюты", callback_data="info_values"
            ),
            InlineKeyboardButton(text="📉 Криптовалюты", callback_data="info_crypto"),
        ],
        [
            InlineKeyboardButton(text="⭐️ Телеграм Звезды", callback_data="info_stars"),
        ],
        [
            InlineKeyboardButton(text="Назад⬅️", callback_data="menu"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# keyboard which returns to regions
def back_info_regions() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Назад⬅️", callback_data="back_to_list_regions")]]
    )
