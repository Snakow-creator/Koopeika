from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# class for settings
class SettingsKeyboard:
    # settings keyboard, and his keyboards
    @staticmethod
    def settings(premium) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(
                    text="Изменить часовой пояс🕰",
                    callback_data="settings_edit_timezone",
                ),
                InlineKeyboardButton(
                    text="Изменить валюту💱", callback_data="settings_edit_value"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Стиль валют", callback_data="settings_edit_style"
                ),
                InlineKeyboardButton(
                    text="Кол-во десятичных знаков", callback_data="settings_edit_nums"
                ),
            ],
        ]
        # if user have a premium subcribe
        if premium:
            buttons.extend(
                [
                    [
                        InlineKeyboardButton(
                            text="Список криптовалют₿",
                            callback_data="settings_edit_cryptomaxcoins",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Koopeika Premium⭐️",
                            callback_data="settings_edit_premium",
                        )
                    ],
                ]
            )

        else:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Koopeika Premium⭐️", callback_data="settings_edit_premium"
                    )
                ]
            )

        buttons.append([InlineKeyboardButton(text="Назад⬅️", callback_data="menu")])

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def change_style() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="Символы", callback_data="style_symbols"),
                InlineKeyboardButton(text="Названия", callback_data="style_codename"),
            ],
            [InlineKeyboardButton(text="Назад⬅️", callback_data="main_profile")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # end settings keyboards

    # back to main menu or profile
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        buttons = [
            [InlineKeyboardButton(text="Главное меню🏠", callback_data="menu")],
            [InlineKeyboardButton(text="Профиль👤", callback_data="main_profile")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def choise_amount() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="Фиаты💵", callback_data="amount_edit_fiat"),
                InlineKeyboardButton(
                    text="Криптовалюты🪙", callback_data="amount_edit_crypto"
                ),
            ],
            [InlineKeyboardButton(text="Назад⬅️", callback_data="main_profile")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def choise_fiat_amount() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="1️⃣", callback_data="fiat_amount_1"),
                InlineKeyboardButton(text="2️⃣", callback_data="fiat_amount_2"),
                InlineKeyboardButton(text="3️⃣", callback_data="fiat_amount_3"),
            ],
            [InlineKeyboardButton(text="Назад⬅️", callback_data="main_profile")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def choise_crypto_amount() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="1️⃣", callback_data="crypto_amount_1"),
                InlineKeyboardButton(text="2️⃣", callback_data="crypto_amount_2"),
                InlineKeyboardButton(text="3️⃣", callback_data="crypto_amount_3"),
            ],
            [
                InlineKeyboardButton(text="4️⃣", callback_data="crypto_amount_4"),
                InlineKeyboardButton(text="5️⃣", callback_data="crypto_amount_5"),
                InlineKeyboardButton(text="6️⃣", callback_data="crypto_amount_6"),
            ],
            [
                InlineKeyboardButton(text="7️⃣", callback_data="crypto_amount_7"),
                InlineKeyboardButton(text="8️⃣", callback_data="crypto_amount_8"),
                InlineKeyboardButton(text="9️⃣", callback_data="crypto_amount_9"),
            ],
            [InlineKeyboardButton(text="Назад⬅️", callback_data="main_profile")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # keyboard for main value
    @staticmethod
    def classic_values() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="🇺🇸USD", callback_data="add_value_pop_USD"),
                InlineKeyboardButton(text="🇪🇺EUR", callback_data="add_value_pop_EUR"),
                InlineKeyboardButton(text="🇷🇺RUB", callback_data="add_value_pop_RUB"),
                InlineKeyboardButton(text="🇦🇪AED", callback_data="add_value_pop_AED"),
            ],
            [
                InlineKeyboardButton(text="🇧🇾BYN", callback_data="add_value_pop_BYN"),
                InlineKeyboardButton(text="🇺🇦UAH", callback_data="add_value_pop_UAH"),
                InlineKeyboardButton(text="🇰🇿KZT", callback_data="add_value_pop_KZT"),
                InlineKeyboardButton(text="🇬🇪GEL", callback_data="add_value_pop_GEL"),
            ],
            [
                InlineKeyboardButton(text="🇨🇳CNY", callback_data="add_value_pop_CNY"),
                InlineKeyboardButton(text="🇯🇵JPY", callback_data="add_value_pop_JPY"),
                InlineKeyboardButton(text="🇹🇷TRY", callback_data="add_value_pop_TRY"),
                InlineKeyboardButton(text="🇬🇧GBP", callback_data="add_value_pop_GBP"),
            ],
            [
                InlineKeyboardButton(
                    text="Остальные валюты", callback_data="otherlist_value_add"
                )
            ],
            [InlineKeyboardButton(text="Назад⬅️", callback_data="main_profile")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def time_zone() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="UTC-12", callback_data="time_zone_-12"),
                InlineKeyboardButton(text="UTC-3", callback_data="time_zone_-3"),
                InlineKeyboardButton(text="UTC+6", callback_data="time_zone_+6"),
            ],
            [
                InlineKeyboardButton(text="UTC-11", callback_data="time_zone_-11"),
                InlineKeyboardButton(text="UTC-2", callback_data="time_zone_-2"),
                InlineKeyboardButton(text="UTC+7", callback_data="time_zone_+7"),
            ],
            [
                InlineKeyboardButton(text="UTC-10", callback_data="time_zone_-10"),
                InlineKeyboardButton(text="UTC-1", callback_data="time_zone_-1"),
                InlineKeyboardButton(text="UTC+8", callback_data="time_zone_+8"),
            ],
            [
                InlineKeyboardButton(text="UTC-9", callback_data="time_zone_-9"),
                InlineKeyboardButton(text="UTC", callback_data="time_zone_±0"),
                InlineKeyboardButton(text="UTC+9", callback_data="time_zone_+9"),
            ],
            [
                InlineKeyboardButton(text="UTC-8", callback_data="time_zone_-8"),
                InlineKeyboardButton(text="UTC+1", callback_data="time_zone_+1"),
                InlineKeyboardButton(text="UTC+10", callback_data="time_zone_+10"),
            ],
            [
                InlineKeyboardButton(text="UTC-7", callback_data="time_zone_-7"),
                InlineKeyboardButton(text="UTC+2", callback_data="time_zone_+2"),
                InlineKeyboardButton(text="UTC+11", callback_data="time_zone_+11"),
            ],
            [
                InlineKeyboardButton(text="UTC-6", callback_data="time_zone_-6"),
                InlineKeyboardButton(text="UTC+3", callback_data="time_zone_+3"),
                InlineKeyboardButton(text="UTC+12", callback_data="time_zone_+12"),
            ],
            [
                InlineKeyboardButton(text="UTC-5", callback_data="time_zone_-5"),
                InlineKeyboardButton(text="UTC+4", callback_data="time_zone_+4"),
                InlineKeyboardButton(text="UTC+13", callback_data="time_zone_+13"),
            ],
            [
                InlineKeyboardButton(text="UTC-4", callback_data="time_zone_-4"),
                InlineKeyboardButton(text="UTC+5", callback_data="time_zone_+5"),
                InlineKeyboardButton(text="UTC+14", callback_data="time_zone_+14"),
            ],
            [InlineKeyboardButton(text="Назад⬅️", callback_data="main_profile")],
        ]

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def crypto_max_coins():
        buttons = [
            [
                InlineKeyboardButton(
                    text="Стандартный(16 валют)", callback_data="crypto_max_16"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Большой(28 валют)", callback_data="crypto_max_28"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Огромный(36 валют)", callback_data="crypto_max_36"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Монструозный(48 валют)", callback_data="crypto_max_48"
                )
            ],
            [InlineKeyboardButton(text="Назад⬅️", callback_data="main_profile")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
