from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

import database.online_config as oc


# add main keyboard
main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Баланс💲")],
        [KeyboardButton(text="Конвертация🏪"), KeyboardButton(text="Список валют📖")],
        [KeyboardButton(text="Активы💸"), KeyboardButton(text="Транзакции🔁")],
        [KeyboardButton(text="Настройки⚙️")],
    ],
    resize_keyboard=True,
    input_field_placeholder="👇🏻👇🏻👇🏻",
)

# assets keyboard
assets = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить активы💸"), KeyboardButton(text="Указать траты📉")],
        [KeyboardButton(text="Назад⬅️")],
    ],
    resize_keyboard=True,
    input_field_placeholder="👇🏻👇🏻👇🏻",
)

# transactions keyboard
trasnactions = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="История транзакций📋"), KeyboardButton(text="Изменить транзакцию📝")],
        [KeyboardButton(text="Назад⬅️")],
    ],
    resize_keyboard=True,
    input_field_placeholder="👇🏻👇🏻👇🏻",
)

#sub_channel - required subscribe
sub_channel = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text="Подписаться на канал", url="https://t.me/obotov")]]
    )

# regions keyboard which under message
def regions() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🌍 Европа", callback_data="info_europe"),
            InlineKeyboardButton(text="🌎 Америка", callback_data="info_america"),
            InlineKeyboardButton(text="🌏Азия", callback_data="info_asia"),
        ],
        [
            InlineKeyboardButton(text="🌍 Африка и Ближний Восток", callback_data="info_africa"),
            InlineKeyboardButton(text="🌊 Океания", callback_data="info_oceania"),
        ],
        [
            InlineKeyboardButton(text="💱 Популярные валюты", callback_data="info_values"),
            InlineKeyboardButton(text="📉 Криптовалюты", callback_data="info_crypto"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# keyboard which returns to regions
back_regions = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад⬅️", callback_data="back_reg")]]
)


# class with buttons under messages
class clbk:
    # assets keyboard, add assets without comment
    @staticmethod
    def no_comment() -> InlineKeyboardMarkup:
        button = [[InlineKeyboardButton(text="Без пояснений❌", callback_data="without_comment")]]
        return InlineKeyboardMarkup(inline_keyboard=button)

    # beautiful keyboard for transactions, change page
    @staticmethod
    def transactions(tg_id) -> InlineKeyboardMarkup:
        page = oc.data_page[tg_id]
        buttons = [
            [
                InlineKeyboardButton(text="⬅️", callback_data="clbk_transaction_left"),
                InlineKeyboardButton(text=f"{page}", callback_data="clbk_transaction_page"),
                InlineKeyboardButton(text="➡️", callback_data="clbk_transaction_right"),
            ]
        ]

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # keyboard for popular values
    @staticmethod
    def popular_values(convertation=False) -> InlineKeyboardMarkup:
        if convertation:
            data = convertation
        else:
            data = "add"
        buttons = [
            [
                InlineKeyboardButton(text="🇺🇸USD", callback_data=f"{data}_value_pop_USD"),
                InlineKeyboardButton(text="🇪🇺EUR", callback_data=f"{data}_value_pop_EUR"),
                InlineKeyboardButton(text="🇷🇺RUB", callback_data=f"{data}_value_pop_RUB"),
                InlineKeyboardButton(text="🇦🇪AED", callback_data=f"{data}_value_pop_AED"),
            ],
            [
                InlineKeyboardButton(text="🇧🇾BYN", callback_data=f"{data}_value_pop_BYN"),
                InlineKeyboardButton(text="🇺🇦UAH", callback_data=f"{data}_value_pop_UAH"),
                InlineKeyboardButton(text="🇰🇿KZT", callback_data=f"{data}_value_pop_KZT"),
                InlineKeyboardButton(text="🇬🇪GEL", callback_data=f"{data}_value_pop_GEL"),
            ],
            [
                InlineKeyboardButton(text="🇨🇳CNY", callback_data=f"{data}_value_pop_CNY"),
                InlineKeyboardButton(text="🇯🇵JPY", callback_data=f"{data}_value_pop_JPY"),
                InlineKeyboardButton(text="🇹🇷TRY", callback_data=f"{data}_value_pop_TRY"),
                InlineKeyboardButton(text="🇬🇧GBP", callback_data=f"{data}_value_pop_GBP"),
            ],
            [
                InlineKeyboardButton(text="₿BTC", callback_data=f"{data}_value_pop_BTC"),
                InlineKeyboardButton(text="ΞETH", callback_data=f"{data}_value_pop_ETH"),
                InlineKeyboardButton(text="SOL", callback_data=f"{data}_value_pop_SOL"),
                InlineKeyboardButton(text="TON", callback_data=f"{data}_value_pop_TON"),
            ],
            [InlineKeyboardButton(text="Остальные валюты", callback_data=f"clbk_otherlist_value_{data}")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # keyboard for full list
    @staticmethod
    def full_list(convertation=False) -> InlineKeyboardMarkup:
        if convertation:
            data = convertation
        else:
            data = "add"
        buttons = [
            [
                InlineKeyboardButton(text="🇦🇺 AUD - Доллар", callback_data=f"{data}_value_full_AUD"),
                InlineKeyboardButton(text="🇦🇿 AZN - Манат", callback_data=f"{data}_value_full_AZN"),
            ],
            [
                InlineKeyboardButton(text="🇧🇷 BRL - Реал", callback_data=f"{data}_value_full_BRL"),
                InlineKeyboardButton(text="🇧🇾 BYN - Рубль", callback_data=f"{data}_value_full_BYN"),
            ],
            [
                InlineKeyboardButton(text="🇨🇦 CAD - Доллар", callback_data=f"{data}_value_full_CAD"),
                InlineKeyboardButton(text="🇨🇭 CHF - Франк", callback_data=f"{data}_value_full_CHF"),
            ],
            [
                InlineKeyboardButton(text="🇨🇳 CNY - Юань", callback_data=f"{data}_value_full_CNY"),
                InlineKeyboardButton(text="🇨🇿 CZK - Крона", callback_data=f"{data}_value_full_CZK"),
            ],
            [
                InlineKeyboardButton(text="🇩🇰 DKK - Крона", callback_data=f"{data}_value_full_DKK"),
                InlineKeyboardButton(text="🇪🇺 EUR - Евро", callback_data=f"{data}_value_full_EUR"),
            ],
            [
                InlineKeyboardButton(text="🇬🇧 GBP - Фунт", callback_data=f"{data}_value_full_GBP"),
                InlineKeyboardButton(text="🇬🇪 GEL - Лари", callback_data=f"{data}_value_full_GEL"),
            ],
            [
                InlineKeyboardButton(text="🇮🇷 IRR - Риал", callback_data=f"{data}_value_full_IRR"),
                InlineKeyboardButton(text="🇮🇳 INR - Рупия", callback_data=f"{data}_value_full_INR"),
            ],
            [
                InlineKeyboardButton(text="🇯🇵 JPY - Йена", callback_data=f"{data}_value_full_JPY"),
                InlineKeyboardButton(text="🇰🇼 KWD - Динар", callback_data=f"{data}_value_full_KWD"),
            ],
            [
                InlineKeyboardButton(text="🇰🇬 KGS - Сом", callback_data=f"{data}_value_full_KGS"),
                InlineKeyboardButton(text="🇰🇷 KRW - Вона", callback_data=f"{data}_value_full_KRW"),
            ],
            [
                InlineKeyboardButton(text="🇲🇾 MYR - Ринггит", callback_data=f"{data}_value_full_MYR"),
                InlineKeyboardButton(text="🇲🇩 MDL - Лей", callback_data=f"{data}_value_full_MDL"),
            ],
            [
                InlineKeyboardButton(text="🇲🇽 MXN - Песо", callback_data=f"{data}_value_full_MXN"),
                InlineKeyboardButton(text="🇳🇴 NOK - Крона", callback_data=f"{data}_value_full_NOK"),
            ],
            [
                InlineKeyboardButton(text="🇵🇱 PLN - Злотый", callback_data=f"{data}_value_full_PLN"),
                InlineKeyboardButton(text="🇷🇺 RUB - Рубль", callback_data=f"{data}_value_full_RUB"),
            ],
            [
                InlineKeyboardButton(text="🇸🇦 SAR - Риял", callback_data=f"{data}_value_full_SAR"),
                InlineKeyboardButton(text="🇸🇬 SGD - Доллар", callback_data=f"{data}_value_full_SGD"),
            ],
            [
                InlineKeyboardButton(text="🇸🇪 SEK - Крона", callback_data=f"{data}_value_full_SEK"),
                InlineKeyboardButton(text="🇹🇭 THB - Бат", callback_data=f"{data}_value_full_THB"),
            ],
            [
                InlineKeyboardButton(text="🇹🇯 TJS - Сомони", callback_data=f"{data}_value_full_TJS"),
                InlineKeyboardButton(text="🇹🇷 TRY - Лира", callback_data=f"{data}_value_full_TRY"),
            ],
            [
                InlineKeyboardButton(text="🇺🇸 USD - Доллар", callback_data=f"{data}_value_full_USD"),
                InlineKeyboardButton(text="🇺🇦 UAH - Гривна", callback_data=f"{data}_value_full_UAH"),
            ],
            [
                InlineKeyboardButton(text="🇺🇿 UZS - Сум", callback_data=f"{data}_value_full_UZS"),
                InlineKeyboardButton(text="🇿🇦 ZAR - Рэнд(ЮАР)", callback_data=f"{data}_value_full_ZAR"),
            ],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # settings keyboard, and his keyboards
    @staticmethod
    def settings() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="Изменить часовой пояс🕰", callback_data="clbk_edit_timezone"),
                InlineKeyboardButton(text="Изменить валюту💱", callback_data="clbk_edit_value"),
            ],
            [InlineKeyboardButton(text="Стиль отображения валют", callback_data="clbk_edit_style")],
            [InlineKeyboardButton(text="Информацияℹ️", callback_data="clbk_edit_info")],
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
            [InlineKeyboardButton(text="Остальные валюты", callback_data="clbk_otherlist_value_add")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def change_style() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="Символы", callback_data="style_symbols"),
                InlineKeyboardButton(text="Названия", callback_data="style_codename"),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # end settings keyboards

    @staticmethod
    def change_transaction() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="Изменить сумму✏️", callback_data="edit_assets"),
                InlineKeyboardButton(text="Удалить транзакцию🗑", callback_data="edit_delete"),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
