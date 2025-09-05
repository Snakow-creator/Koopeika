from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            KeyboardButton, ReplyKeyboardMarkup)

from loggers.logs import log

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

# sub_channel - required subscribe
sub_channel = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/obotov")]]
)


# class for convertation and assets buttons
class con:
    # keyboard for popular values
    @staticmethod
    def popular_values(premium, convertation=False) -> InlineKeyboardMarkup:
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
                InlineKeyboardButton(text="⭐️", callback_data=f"{data}_value_pop_⭐️"),
            ],
            [
                InlineKeyboardButton(text="₿BTC", callback_data=f"{data}_value_pop_BTC"),
                InlineKeyboardButton(text="ΞETH", callback_data=f"{data}_value_pop_ETH"),
                InlineKeyboardButton(text="SOL", callback_data=f"{data}_value_pop_SOL"),
                InlineKeyboardButton(text="TON", callback_data=f"{data}_value_pop_TON"),
            ],
        ]
        if premium:
            buttons.append([
                InlineKeyboardButton(text="Криптовалюты", callback_data=f"cryptolist_value_{data}"),
                InlineKeyboardButton(text="Остальные валюты", callback_data=f"otherlist_value_{data}"),
            ])
        else:
            buttons.append([
                InlineKeyboardButton(text="Остальные валюты", callback_data=f"otherlist_value_{data}"),
            ])
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def stars_popular_values():
        buttons = [
            [
                InlineKeyboardButton(text="🇺🇸USD", callback_data=f"endcon_value_pop_USD"),
                InlineKeyboardButton(text="🇪🇺EUR", callback_data=f"endcon_value_pop_EUR"),
                InlineKeyboardButton(text="🇷🇺RUB", callback_data=f"endcon_value_pop_RUB"),
                InlineKeyboardButton(text="🇦🇪AED", callback_data=f"endcon_value_pop_AED"),
            ],
            [
                InlineKeyboardButton(text="🇧🇾BYN", callback_data=f"endcon_value_pop_BYN"),
                InlineKeyboardButton(text="🇺🇦UAH", callback_data=f"endcon_value_pop_UAH"),
                InlineKeyboardButton(text="🇰🇿KZT", callback_data=f"endcon_value_pop_KZT"),
                InlineKeyboardButton(text="🇬🇪GEL", callback_data=f"endcon_value_pop_GEL"),
            ],
            [
                InlineKeyboardButton(text="🇨🇳CNY", callback_data=f"endcon_value_pop_CNY"),
                InlineKeyboardButton(text="🇯🇵JPY", callback_data=f"endcon_value_pop_JPY"),
                InlineKeyboardButton(text="🇹🇷TRY", callback_data=f"endcon_value_pop_TRY"),
                InlineKeyboardButton(text="TON", callback_data="endcon_value_pop_TON"),
            ],
            [InlineKeyboardButton(text="Остальные валюты", callback_data=f"otherlist_value_endcon")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # keyboard for full list
    @staticmethod
    def full_list_values(convertation=False) -> InlineKeyboardMarkup:
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
            [
                InlineKeyboardButton(text="Назад⬅️", callback_data=f"value_back_{data}"),
            ],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def crypto_values(max_coins, convertation=False) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        cryptolist = list(oc.cryptorates.keys())
        if convertation:
            data = convertation
        else:
            data = "add"

        for value in cryptolist[:max_coins]:
            log.debug(value)
            builder.button(text=f"{value[:3]}", callback_data=f"{data}_value_cpt_{value}")

        builder.button(text="Назад⬅️", callback_data=f"value_back_{data}")
        builder.adjust(4)
        return builder.as_markup()

    @staticmethod
    def stars_choise():
        buttons = [
            [
                InlineKeyboardButton(text="⭐️(покупка)", callback_data="con_value_pop_⭐️buy"),
                InlineKeyboardButton(text="⭐️(продажа)", callback_data="con_value_pop_⭐️sell"),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # fast input number for convertation
    @staticmethod
    def input_numbers(sym: str) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text=f"1{sym}", callback_data="con_input_amount_1"),
                InlineKeyboardButton(text=f"100{sym}", callback_data="con_input_amount_100"),
                InlineKeyboardButton(text=f"1000{sym}", callback_data="con_input_amount_1000"),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)


# class for other inline buttons
class clbk:
    # assets keyboard, add assets without comment
    @staticmethod
    def no_comment() -> InlineKeyboardMarkup:
        button = [[InlineKeyboardButton(text="Без пояснений❌", callback_data="without_comment")]]
        return InlineKeyboardMarkup(inline_keyboard=button)

    # beautiful keyboard for transactions, change page
    @staticmethod
    def transactions(tg_id) -> InlineKeyboardMarkup:
        page = oc.Profile.get(tg_id).transactions_page
        buttons = [
            [
                InlineKeyboardButton(text="⬅️", callback_data="transaction_left"),
                InlineKeyboardButton(text=f"{page}", callback_data="transaction_page"),
                InlineKeyboardButton(text="➡️", callback_data="transaction_right"),
            ]
        ]

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # regions keyboard which under message
    @staticmethod
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
            [
                InlineKeyboardButton(text="⭐️ Телеграм Звезды", callback_data="info_stars"),
            ],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # keyboard which returns to regions
    def back_regions() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Назад⬅️", callback_data="back_reg")]]
        )


# class for settings
class set:
    # settings keyboard, and his keyboards
    @staticmethod
    def settings(premium) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="Изменить часовой пояс🕰", callback_data="settings_edit_timezone"),
                InlineKeyboardButton(text="Изменить валюту💱", callback_data="settings_edit_value"),
            ],
            [
                InlineKeyboardButton(text="Стиль валют", callback_data="settings_edit_style"),
                InlineKeyboardButton(text="Кол-во десятичных знаков", callback_data="settings_edit_nums"),
            ],
        ]
        if premium:
            buttons.append([InlineKeyboardButton(text="Список криптовалют₿", callback_data="settings_edit_cryptomaxcoins")])
        row = [InlineKeyboardButton(text="Koopeika Premium⭐️", callback_data="settings_edit_premium"),
               InlineKeyboardButton(text="Информацияℹ️", callback_data="settings_edit_info")]
        buttons.append(row)

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
    def edit_transaction() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="Изменить сумму✏️", callback_data="edit_assets"),
                InlineKeyboardButton(text="Удалить транзакцию🗑", callback_data="edit_delete"),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def choise_amount() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="Фиаты💵", callback_data="amount_edit_fiat"),
                InlineKeyboardButton(text="Криптовалюты🪙", callback_data="amount_edit_crypto"),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def choise_fiat_amount() -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(text="1️⃣", callback_data="fiat_amount_1"),
                InlineKeyboardButton(text="2️⃣", callback_data="fiat_amount_2"),
                InlineKeyboardButton(text="3️⃣", callback_data="fiat_amount_3"),
            ]
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
            [InlineKeyboardButton(text="Остальные валюты", callback_data="otherlist_value_add")],
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

    @staticmethod
    def crypto_max_coins():
        buttons = [
                [InlineKeyboardButton(text="Стандартный(16 валют)", callback_data="crypto_max_16")],
                [InlineKeyboardButton(text="Большой(28 валют)", callback_data="crypto_max_28")],
                [InlineKeyboardButton(text="Огромный(36 валют)", callback_data="crypto_max_36")],
                [InlineKeyboardButton(text="Монструозный(48 валют)", callback_data="crypto_max_48")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)


class pay:
    @staticmethod
    def premium_buttons():
        builder = InlineKeyboardBuilder()
        builder.button(text="1 месяц", callback_data="pay_premium_month_stars")
        builder.button(text="Условия пользования", callback_data="terms_of_service")
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def terms_of_services_back():
        builder = InlineKeyboardBuilder()
        builder.button(text="Назад⬅️", callback_data="settings_edit_premium")
        return builder.as_markup()

    @staticmethod
    def premium():
        builder = InlineKeyboardBuilder()
        builder.button(text="Подписаться на месяц(1⭐️)", pay=True)
        return builder.as_markup()
