import database.requests as rq


async def con_balance(tg_id: int, rates: dict):
    result = 0
    trs = await rq.Transactions.history_transactions(tg_id)
    value = await rq.get_value(tg_id)
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
    await rq.Balance.edit(tg_id, result)
    return result


# промежуточная конвертация между криптовалютой и usdt
async def convert_to_usdt(amount, from_currency, rates):
    if from_currency == "USD":
        return amount
    from_rate = rates["USD"]
    to_rate = rates[from_currency]
    return (amount / from_rate) * to_rate


async def convert_currency(amount, from_currency, to_currency, rates):
    amount = float(amount)
    # if input assets are the same as the output assets
    if from_currency == to_currency:
        return amount

    # Fiat -> Fiat
    if (from_currency in rates) and (to_currency in rates):
        from_rate = rates[to_currency]
        to_rate = rates[from_currency]
        return format((amount / from_rate) * to_rate, ".3f")

    # Fiat -> Crypto
    elif (from_currency in rates) and (to_currency not in rates):
        amount_in_usdt = await convert_to_usdt(amount, from_currency, rates)
        enter_amount = amount_in_usdt / await get_conversion_rate("USDT", to_currency)
        return format(enter_amount, ".9f")

    # Crypto -> Fiat
    elif (from_currency not in rates) and (to_currency in rates):
        usd_rate = rates["USD"]
        to_rate = rates[to_currency]
        crypto_to_usdt = await get_conversion_rate(from_currency, "USDT")  # цена крипты
        amount_in_usdt = crypto_to_usdt * amount
        enter_amount = (amount_in_usdt / to_rate) * usd_rate
        return format(enter_amount, ".3f")

    # Crypto -> Crypto
    elif (from_currency not in rates) and (to_currency not in rates):
        crypto_to_usdt = await get_conversion_rate(from_currency, "USDT")
        amount_in_usdt = crypto_to_usdt * amount
        usdt_in_crypto = await get_conversion_rate("USDT", to_currency)
        enter_amount = amount_in_usdt / usdt_in_crypto
        return format(enter_amount, ".9f")

    raise ValueError


async def get_conversion_rate(from_currency, to_currency):
    from database.online_config import cryptorates

    try:
        pair = f"{from_currency}{to_currency}".upper()
        if pair in cryptorates.keys():
            return cryptorates[pair]
        return await get_conversion_rate(to_currency, from_currency)

    except Exception as e:
        raise ValueError(f"Неизвестная ошибка: {str(e)}")
