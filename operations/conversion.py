import database.requests as rq

from loggers.logs import log


async def con_balance(tg_id: int, rates: dict):
    result = 0
    trs_obj = await rq.Transactions.load(tg_id)
    trs = trs_obj.transactions
    value = trs_obj.user.value
    for tr in trs:
        op = tr.amount[0]
        amount = float(tr.amount[1:])
        from_value = tr.value
        res = await convert_currency(amount, from_value, value, rates)
        if op == "+":
            result += float(res)
        elif op == "-":
            result -= float(res)

    result = "{:,.2f}".format(result)
    await rq.Balance.change(tg_id, result)
    return result


# промежуточная конвертация между криптовалютой и usdt
async def convert_to_usdt(amount, to_currency, rates):
    if to_currency == "USD":
        return amount
    from_rate = rates["USD"]
    to_rate = rates[to_currency]
    return (amount / from_rate) * to_rate


async def convert_currency(amount, from_currency, to_currency, rates):
    amount = float(amount)
    crypto_bool_to = (to_currency not in rates) and (to_currency[0:2] != "⭐️")
    crypto_bool_from = (from_currency not in rates) and (from_currency[0:2] != "⭐️")
    # if input assets are the same as the output assets
    if from_currency == to_currency:
        return str(amount)

    # Fiat -> Fiat
    if (from_currency in rates) and (to_currency in rates):
        to_rate = rates[to_currency]
        from_rate = rates[from_currency]
        return format((amount / to_rate) * from_rate, ".3f")

    # Fiat -> Crypto
    elif (from_currency in rates) and (crypto_bool_to):
        amount_in_usdt = await convert_to_usdt(amount, from_currency, rates)
        result = amount_in_usdt / await get_conversion_rate(to_currency, "USDT")
        return format(result, ".9f")

    # Crypto -> Fiat
    elif (crypto_bool_from) and (to_currency in rates):
        usd_rate = rates["USD"]
        to_rate = rates[to_currency]
        crypto_to_usdt = await get_conversion_rate(from_currency, "USDT")  # цена крипты
        amount_in_usdt = crypto_to_usdt * amount
        result = (amount_in_usdt / to_rate) * usd_rate
        return format(result, ".3f")

    # Crypto -> Crypto
    elif (crypto_bool_from) and (crypto_bool_to):
        crypto_to_usdt = await get_conversion_rate(from_currency, "USDT")
        amount_in_usdt = crypto_to_usdt * amount
        usdt_in_crypto = await get_conversion_rate("USDT", to_currency)
        result = amount_in_usdt / usdt_in_crypto
        return format(result, ".9f")

    # Stars -> Fiat
    elif (from_currency[0:2] == "⭐️") and (to_currency in rates):
        if from_currency[-3:] == "buy":
            stars_currency = 0.015
        elif from_currency[-4:] == "sell" or from_currency == "⭐️":
            stars_currency = 0.013
        usd_amount = amount * stars_currency
        usd_rate = rates["USD"]
        to_rate = rates[to_currency]
        result = (usd_amount / to_rate) * usd_rate
        return format(result, ".3f")

    # Stars -> Crypto
    elif (from_currency[0:2] == "⭐️") and (crypto_bool_to):
        if from_currency[-3:] == "buy":
            stars_currency = 0.015
        elif from_currency[-4:] == "sell" or from_currency == "⭐️":
            stars_currency = 0.013
        usd_amount = stars_currency * amount
        result = usd_amount / await get_conversion_rate(to_currency, "USDT")
        return format(result, ".9f")

    # Fiat -> USD -> Stars
    elif (from_currency in rates) and (to_currency == "⭐️"):
        usd_rate = rates["USD"]
        from_rate = rates[from_currency]
        usd_amount = (amount / usd_rate) * from_rate
        return str(usd_amount / 0.015)

    # Crypto -> Stars
    elif (crypto_bool_from) and (to_currency == "⭐️"):
        crypto_to_usdt = await get_conversion_rate(from_currency, "USDT")
        amount_in_usdt = crypto_to_usdt * amount
        return str(amount_in_usdt / 0.015)

    raise ValueError


async def get_conversion_rate(from_currency, to_currency):
    from database.online_config import cryptorates

    try:
        pair = f"{from_currency}{to_currency}".upper()
        if pair in cryptorates.keys():
            return cryptorates[pair]
        return await get_conversion_rate(to_currency, from_currency)

    except Exception as ex:
        log.error(f"Неизвестная ошибка: {ex}")


# convert to true num
async def convert_num(num: str, to_value: str, user_id: int) -> str:
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
