import database.requests as rq
import database.online_config as oc

from loggers.logs import log


class Conversion:
    def __init__(self, from_amount, to_amount):
        self.from_amount = from_amount
        self.to_amount = to_amount

    def text(self, from_symbol, to_symbol):
        from_symbol = self._format_to_LTR(from_symbol)
        return f"Конвертация: {self.from_amount:,}{from_symbol} = {self.to_amount}{to_symbol}"

    @classmethod
    async def conversion(cls, user_id, from_value, to_value, amount, rates):
        converted_amount = await cls._current_currency(from_value, to_value, amount, rates)
        to_amount = await cls._convert_num(converted_amount, to_value, user_id)
        return cls(amount, to_amount)

    @classmethod
    async def _current_currency(cls, from_currency, to_currency, amount, rates):
        amount = float(amount)
        crypto_bool_to = (to_currency not in rates) and (to_currency[0:2] != "⭐️")
        crypto_bool_from = (from_currency not in rates) and (from_currency[0:2] != "⭐️")
        stars_to_stars = (to_currency[0:2] == "⭐️") and (from_currency[0:2] == "⭐️")
        # if input assets are the same as the output assets
        if (from_currency == to_currency) or stars_to_stars:
            log.debug("same assets")
            return amount

        # Fiat -> Fiat
        if (from_currency in rates) and (to_currency in rates):
            log.debug("Fiat -> Fiat")
            to_rate = rates[to_currency]
            from_rate = rates[from_currency]
            converted_amount = format((amount / to_rate) * from_rate, ".3f")

        # Fiat -> Crypto
        elif (from_currency in rates) and (crypto_bool_to):
            log.debug("Fiat -> Crypto")
            amount_in_usdt = await cls._convert_to_usdt(amount, from_currency, rates)
            result = amount_in_usdt / await cls._get_conversion_rate(to_currency)
            converted_amount = format(result, ".9f")

        # Crypto -> Fiat
        elif (crypto_bool_from) and (to_currency in rates):
            log.debug("Crypto -> Fiat")
            usd_rate = rates["USD"]
            to_rate = rates[to_currency]
            crypto_to_usdt = await cls._get_conversion_rate(from_currency)  # цена крипты
            amount_in_usdt = crypto_to_usdt * amount
            result = (amount_in_usdt / to_rate) * usd_rate
            converted_amount = format(result, ".3f")

        # Crypto -> Crypto
        elif (crypto_bool_from) and (crypto_bool_to):
            log.debug("Crypto -> Crypto")
            crypto_to_usdt = await cls._get_conversion_rate(from_currency)
            amount_in_usdt = crypto_to_usdt * amount
            usdt_in_crypto = await cls._get_conversion_rate(to_currency)
            result = amount_in_usdt / usdt_in_crypto
            converted_amount = format(result, ".9f")

        # Stars -> Fiat
        elif (from_currency[0:2] == "⭐️") and (to_currency in rates):
            log.debug("Stars -> Fiat")
            if from_currency[-3:] == "buy":
                stars_currency = 0.015
            elif from_currency[-4:] == "sell" or from_currency == "⭐️":
                stars_currency = 0.013
            usd_amount = amount * stars_currency
            usd_rate = rates["USD"]
            to_rate = rates[to_currency]
            result = (usd_amount / to_rate) * usd_rate
            converted_amount = format(result, ".3f")

        # Stars -> Crypto
        elif (from_currency[0:2] == "⭐️") and (crypto_bool_to):
            log.debug("Stars -> Crypto")
            if from_currency[-3:] == "buy":
                stars_currency = 0.015
            elif from_currency[-4:] == "sell" or from_currency == "⭐️":
                stars_currency = 0.013
            usd_amount = stars_currency * amount
            result = usd_amount / await cls._get_conversion_rate(to_currency)
            converted_amount = format(result, ".9f")

        # Fiat -> USD -> Stars
        elif (from_currency in rates) and (to_currency == "⭐️"):
            log.debug("Fiat -> Stars")
            usd_rate = rates["USD"]
            from_rate = rates[from_currency]
            usd_amount = (amount / usd_rate) * from_rate
            converted_amount = str(usd_amount / 0.015)

        # Crypto -> Stars
        elif (crypto_bool_from) and (to_currency == "⭐️"):
            log.debug("Crypto -> Stars")
            crypto_to_usdt = await cls._get_conversion_rate(from_currency)
            amount_in_usdt = crypto_to_usdt * amount
            converted_amount = format(amount_in_usdt / 0.015, ".9f")

        return converted_amount

    @classmethod
    async def _convert_to_usdt(cls, amount, to_currency, rates):
        if to_currency == "USD":
            return amount
        from_rate = rates["USD"]
        to_rate = rates[to_currency]
        return (amount / from_rate) * to_rate

    @classmethod
    async def _get_conversion_rate(cls, pair):
        from database.online_config import cryptorates

        return cryptorates[pair]

    # convert to true num
    @classmethod
    async def _convert_num(cls, num: str, to_value: str, user_id: int) -> str:
        i = num.find(".")
        user_obj = await rq.SelectUser.load(user_id)
        user = user_obj.user
        fiat_len, crypto_len = user.fiat_amount, user.crypto_amount

        # if num is int converted to float or num is stars
        if (num[-2:] == ".0") or (to_value == "⭐️"):
            res = "{:,}".format(int(float(num)))
            return res
        # if num is rates currency
        elif len(num[(i + 1) :]) == 3:
            res = "{:,.{s}f}".format(float(num), s=fiat_len)
            return res
        # if num is crypto currency
        elif len(num[(i + 1) :]) == 9:
            res = "{:,.{s}f}".format(float(num), s=crypto_len)
            return res

        raise ValueError

    @classmethod
    def _format_to_LTR(self, value):
        if value in ("د.إ", "﷼", "د.ك", "﷼"):
            return f"\u2067{value}\u2069"
        return value


class Convert_Balance(Conversion):
    def __init__(self, result):
        self.balance = result

    @classmethod
    async def con_balance(cls, tg_id: int, rates: dict):
        result = 0
        trs_obj = await rq.Transactions.load(tg_id)
        trs = trs_obj.transactions
        to_value = trs_obj.user.value
        for tr in trs:
            op = tr.amount[0]
            amount = float(tr.amount[1:])
            from_value = tr.value
            convert_amount = await cls._current_currency(from_value, to_value, amount, rates)
            if op == "+":
                result += float(convert_amount)
            elif op == "-":
                result -= float(convert_amount)

        result = "{:,.2f}".format(result)
        await rq.Balance.change(tg_id, result)
        return cls(result)
