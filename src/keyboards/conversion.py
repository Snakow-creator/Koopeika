from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import conf
from tasks.logger import log


# class for convertation and assets buttons
class ConversionKeyboard:
    # keyboard for popular values
    @staticmethod
    def popular_values(premium, convertation=False) -> InlineKeyboardMarkup:
        if convertation:
            data = convertation
        else:
            data = "add"
        buttons = [
            [
                InlineKeyboardButton(
                    text="🇺🇸USD", callback_data=f"{data}_value_pop_USD"
                ),
                InlineKeyboardButton(
                    text="🇪🇺EUR", callback_data=f"{data}_value_pop_EUR"
                ),
                InlineKeyboardButton(
                    text="🇷🇺RUB", callback_data=f"{data}_value_pop_RUB"
                ),
                InlineKeyboardButton(
                    text="🇦🇪AED", callback_data=f"{data}_value_pop_AED"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇧🇾BYN", callback_data=f"{data}_value_pop_BYN"
                ),
                InlineKeyboardButton(
                    text="🇺🇦UAH", callback_data=f"{data}_value_pop_UAH"
                ),
                InlineKeyboardButton(
                    text="🇰🇿KZT", callback_data=f"{data}_value_pop_KZT"
                ),
                InlineKeyboardButton(
                    text="🇬🇪GEL", callback_data=f"{data}_value_pop_GEL"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇨🇳CNY", callback_data=f"{data}_value_pop_CNY"
                ),
                InlineKeyboardButton(
                    text="🇯🇵JPY", callback_data=f"{data}_value_pop_JPY"
                ),
                InlineKeyboardButton(
                    text="🇹🇷TRY", callback_data=f"{data}_value_pop_TRY"
                ),
                InlineKeyboardButton(text="⭐️", callback_data=f"{data}_value_pop_⭐️"),
            ],
            [
                InlineKeyboardButton(
                    text="₿BTC", callback_data=f"{data}_value_pop_BTC"
                ),
                InlineKeyboardButton(
                    text="ΞETH", callback_data=f"{data}_value_pop_ETH"
                ),
                InlineKeyboardButton(text="SOL", callback_data=f"{data}_value_pop_SOL"),
                InlineKeyboardButton(text="TON", callback_data=f"{data}_value_pop_TON"),
            ],
        ]
        if premium:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Криптовалюты", callback_data=f"cryptolist_value_{data}"
                    ),
                    InlineKeyboardButton(
                        text="Остальные валюты", callback_data=f"otherlist_value_{data}"
                    ),
                ]
            )
        else:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Остальные валюты", callback_data=f"otherlist_value_{data}"
                    ),
                ]
            )
        buttons.extend(
            [
                [
                    InlineKeyboardButton(
                        text="Указать криптовалюту в сообщениях",
                        callback_data=f"input_crypto_{data}",
                    )
                ],
                [InlineKeyboardButton(text="Главное меню🏠", callback_data="menu")],
            ]
        )
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def stars_popular_values(premium_user: str | None) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🇺🇸USD", callback_data=f"endcon_value_pop_USD"
                ),
                InlineKeyboardButton(
                    text="🇪🇺EUR", callback_data=f"endcon_value_pop_EUR"
                ),
                InlineKeyboardButton(
                    text="🇷🇺RUB", callback_data=f"endcon_value_pop_RUB"
                ),
                InlineKeyboardButton(
                    text="🇦🇪AED", callback_data=f"endcon_value_pop_AED"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇧🇾BYN", callback_data=f"endcon_value_pop_BYN"
                ),
                InlineKeyboardButton(
                    text="🇺🇦UAH", callback_data=f"endcon_value_pop_UAH"
                ),
                InlineKeyboardButton(
                    text="🇰🇿KZT", callback_data=f"endcon_value_pop_KZT"
                ),
                InlineKeyboardButton(
                    text="🇬🇪GEL", callback_data=f"endcon_value_pop_GEL"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇨🇳CNY", callback_data=f"endcon_value_pop_CNY"
                ),
                InlineKeyboardButton(
                    text="🇯🇵JPY", callback_data=f"endcon_value_pop_JPY"
                ),
                InlineKeyboardButton(
                    text="🇹🇷TRY", callback_data=f"endcon_value_pop_TRY"
                ),
            ],
        ]
        if premium_user:
            buttons[-1].append(
                InlineKeyboardButton(
                    text="🇬🇧GBP", callback_data=f"endcon_value_pop_GBP"
                ),
            )
            buttons.extend(
                [
                    [
                        InlineKeyboardButton(
                            text="₿BTC", callback_data=f"endcon_value_pop_BTC"
                        ),
                        InlineKeyboardButton(
                            text="ΞETH", callback_data=f"endcon_value_pop_ETH"
                        ),
                        InlineKeyboardButton(
                            text="SOL", callback_data=f"endcon_value_pop_SOL"
                        ),
                        InlineKeyboardButton(
                            text="TON", callback_data=f"endcon_value_pop_TON"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="Криптовалюты",
                            callback_data=f"cryptolist_value_endcon",
                        ),
                    ],
                ]
            )
        else:
            buttons[-1].append(
                InlineKeyboardButton(text="TON", callback_data=f"endcon_value_pop_TON"),
            )

        # extend for everything users
        buttons.extend(
            [
                [
                    InlineKeyboardButton(
                        text="Остальные валюты", callback_data=f"otherlist_value_endcon"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Главное меню🏠", callback_data="menu"),
                ],
            ]
        )

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
                InlineKeyboardButton(
                    text="🇦🇺 AUD - Доллар", callback_data=f"{data}_value_full_AUD"
                ),
                InlineKeyboardButton(
                    text="🇦🇿 AZN - Манат", callback_data=f"{data}_value_full_AZN"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇧🇷 BRL - Реал", callback_data=f"{data}_value_full_BRL"
                ),
                InlineKeyboardButton(
                    text="🇧🇾 BYN - Рубль", callback_data=f"{data}_value_full_BYN"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇨🇦 CAD - Доллар", callback_data=f"{data}_value_full_CAD"
                ),
                InlineKeyboardButton(
                    text="🇨🇭 CHF - Франк", callback_data=f"{data}_value_full_CHF"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇨🇳 CNY - Юань", callback_data=f"{data}_value_full_CNY"
                ),
                InlineKeyboardButton(
                    text="🇨🇿 CZK - Крона", callback_data=f"{data}_value_full_CZK"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇩🇰 DKK - Крона", callback_data=f"{data}_value_full_DKK"
                ),
                InlineKeyboardButton(
                    text="🇪🇺 EUR - Евро", callback_data=f"{data}_value_full_EUR"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇬🇧 GBP - Фунт", callback_data=f"{data}_value_full_GBP"
                ),
                InlineKeyboardButton(
                    text="🇬🇪 GEL - Лари", callback_data=f"{data}_value_full_GEL"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇮🇷 IRR - Риал", callback_data=f"{data}_value_full_IRR"
                ),
                InlineKeyboardButton(
                    text="🇮🇳 INR - Рупия", callback_data=f"{data}_value_full_INR"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇯🇵 JPY - Йена", callback_data=f"{data}_value_full_JPY"
                ),
                InlineKeyboardButton(
                    text="🇰🇼 KWD - Динар", callback_data=f"{data}_value_full_KWD"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇰🇬 KGS - Сом", callback_data=f"{data}_value_full_KGS"
                ),
                InlineKeyboardButton(
                    text="🇰🇷 KRW - Вона", callback_data=f"{data}_value_full_KRW"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇲🇾 MYR - Ринггит", callback_data=f"{data}_value_full_MYR"
                ),
                InlineKeyboardButton(
                    text="🇲🇩 MDL - Лей", callback_data=f"{data}_value_full_MDL"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇲🇽 MXN - Песо", callback_data=f"{data}_value_full_MXN"
                ),
                InlineKeyboardButton(
                    text="🇳🇴 NOK - Крона", callback_data=f"{data}_value_full_NOK"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇵🇱 PLN - Злотый", callback_data=f"{data}_value_full_PLN"
                ),
                InlineKeyboardButton(
                    text="🇷🇺 RUB - Рубль", callback_data=f"{data}_value_full_RUB"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇸🇦 SAR - Риял", callback_data=f"{data}_value_full_SAR"
                ),
                InlineKeyboardButton(
                    text="🇸🇬 SGD - Доллар", callback_data=f"{data}_value_full_SGD"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇸🇪 SEK - Крона", callback_data=f"{data}_value_full_SEK"
                ),
                InlineKeyboardButton(
                    text="🇹🇭 THB - Бат", callback_data=f"{data}_value_full_THB"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇹🇯 TJS - Сомони", callback_data=f"{data}_value_full_TJS"
                ),
                InlineKeyboardButton(
                    text="🇹🇷 TRY - Лира", callback_data=f"{data}_value_full_TRY"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇺🇸 USD - Доллар", callback_data=f"{data}_value_full_USD"
                ),
                InlineKeyboardButton(
                    text="🇺🇦 UAH - Гривна", callback_data=f"{data}_value_full_UAH"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🇺🇿 UZS - Сум", callback_data=f"{data}_value_full_UZS"
                ),
                InlineKeyboardButton(
                    text="🇿🇦 ZAR - Рэнд(ЮАР)", callback_data=f"{data}_value_full_ZAR"
                ),
            ],
            [
                InlineKeyboardButton(text="Назад⬅️", callback_data=f"value_back_{data}"),
            ],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def back_button(data="con"):
        button = [
            [InlineKeyboardButton(text="Назад⬅️", callback_data=f"value_back_{data}")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=button)

    @staticmethod
    def crypto_values(max_coins, convertation=False) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        cryptolist = list(conf.cryptorates.keys())
        if convertation:
            data = convertation
        else:
            data = "add"

        for value in cryptolist[:max_coins]:
            log.debug(value)
            builder.button(
                text=f"{value[:3]}", callback_data=f"{data}_value_cpt_{value}"
            )

        builder.button(text="Назад⬅️", callback_data=f"value_back_{data}")
        builder.adjust(4)
        return builder.as_markup()

    @staticmethod
    def stars_choise():
        buttons = [
            [
                InlineKeyboardButton(
                    text="⭐️(покупка)", callback_data="con_value_pop_⭐️buy"
                ),
                InlineKeyboardButton(
                    text="⭐️(продажа)", callback_data="con_value_pop_⭐️sell"
                ),
            ],
            [
                InlineKeyboardButton(text="Назад⬅️", callback_data="value_back_con"),
            ],
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # fast input number for convertation
    @staticmethod
    def input_numbers(sym: str) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(
                    text=f"1{sym}", callback_data="con_input_amount_1"
                ),
                InlineKeyboardButton(
                    text=f"100{sym}", callback_data="con_input_amount_100"
                ),
                InlineKeyboardButton(
                    text=f"1000{sym}", callback_data="con_input_amount_1000"
                ),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
