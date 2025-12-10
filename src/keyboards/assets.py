from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class AssetsKeyboard:
    @staticmethod
    def assets_keyboard() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(
                    text="Добавить активы💸", callback_data="add_assets_change"
                ),
                InlineKeyboardButton(
                    text="Указать траты📉", callback_data="add_assets_deprive"
                ),
            ],
            [InlineKeyboardButton(text="Назад⬅️", callback_data="menu")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    # assets keyboard, add assets without comment
    def no_comment() -> InlineKeyboardMarkup:
        button = [
            [
                InlineKeyboardButton(
                    text="Без пояснений❌", callback_data="without_comment"
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=button)
