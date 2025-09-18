import requests
import aiohttp

import xml.etree.ElementTree as ES
import database.requests as rq

from secret.config import NBK_API, CRYPTO_API, CRYPTO_TOP_API, static_cryptolist
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
async def get_cryptorates(list_currency: list):
    crates = {}
    async with aiohttp.ClientSession() as session:
        url = CRYPTO_API
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                crates_dict = {coin["symbol"]: coin["price"] for coin in data}
                for currency in list_currency:
                    coin = currency + "USDT"
                    if coin in crates_dict.keys():
                        crates[currency] = float(crates_dict[coin])
                return crates
            else:
                log.error("error with parsing data get_cryptorate")


# add crypto to cryptolist
async def parse_crypto_top():
    din_cryptolist = []
    async with aiohttp.ClientSession() as session:
        url = CRYPTO_TOP_API
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
            else:
                log.error(f"Error with parsing data: {response.status}")
            symbols_list = [coin["symbol"] for coin in data if float(coin["lastPrice"])]
            for coin in symbols_list:
                if coin[-4:] == "USDT" and coin[:-4] not in static_cryptolist:
                    din_cryptolist.append(coin[:-4])
            dinamic_cryptolist = static_cryptolist + din_cryptolist
            return dinamic_cryptolist


# get data cryptorates
async def cryptorates():
    dinamic_cryptolist = await parse_crypto_top()
    rq_values = await rq.Transactions.get_values()
    full_list = dinamic_cryptolist + rq_values
    crates = await get_cryptorates(full_list)
    return crates
