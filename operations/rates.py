import requests

import xml.etree.ElementTree as ES

from secret.config import NBK_API, CRYPTO_API, static_cryptolist
from loggers.logs import log


# country values
def get_exchange_rates():
    rates = {"KZT": 1}
    res = requests.get(NBK_API)
    res = res.text
    root = ES.fromstring(res)
    items = root.find("channel").findall("item")
    for item in items:
        rates[item.findtext("title")] = float(item.findtext("description"))
    log.debug(f"Get exchange rates")
    return rates


# cryptovalues
def get_cryptorate(currency):
    pair = f"{currency}".upper()
    url = f"{CRYPTO_API}?symbol={pair}"
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        if "price" in data:
            price = data["price"]
        return float(price)


def get_cryptorates():
    crates = {}
    global static_cryptolist
    for crypto in static_cryptolist:
        res = get_cryptorate(crypto)
        crates[crypto] = res
    log.debug(f"Get cryptorates")
    return crates


# add crypto to cryptolist
def add_crypto(max_coins:int=6):
    din_cryptolist = []
    url = "https://api.binance.com/api/v3/ticker/24hr"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        symbols_list = [coin["symbol"] for coin in data]

        for coin in symbols_list:
            if coin[-4:] == "USDT" and coin not in static_cryptolist:
                din_cryptolist.append(coin)
    log.debug(f"Get cryptolist")
    return din_cryptolist[:max_coins]
