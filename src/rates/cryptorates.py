from config.secret import CRYPTO_API, CRYPTO_TOP_API, static_cryptolist

from tasks.logger import log

import requests
import aiohttp


# base cryptorates
async def get_cryptorates(list_currency: list):
    crates = {}
    # init aiohttp and get data
    async with aiohttp.ClientSession() as session:
        url = CRYPTO_API
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()

                # create dict with "symbolUSDT": "price"
                crates_dict = {coin["symbol"]: coin["price"] for coin in data}

                # add necessary rate in crates
                for currency in list_currency:
                    coin = currency + "USDT"
                    if coin in crates_dict.keys():
                        crates[currency] = float(crates_dict[coin])

                return crates
            else:
                log.error("error with parsing data get_cryptorate")


# add crypto to cryptolist keyboard
def parse_top_cryptorates():
    din_cryptolist = []

    # init aiohttp and get data
    url = CRYPTO_TOP_API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

    # create top dinamic cryptolist
    else:
        log.error(f"Error with parsing data: {response.status}")

    # sort rates which more than 0
    symbols_list = [coin["symbol"] for coin in data if float(coin["lastPrice"])]

    # sort cryptolist and add dinamic cryptolist
    for coin in symbols_list:
        if coin[-4:] == "USDT" and coin[:-4] not in static_cryptolist:
            din_cryptolist.append(coin[:-4])

    # unite static list and top dinamic cryptolist and return his
    dinamic_cryptolist = static_cryptolist + din_cryptolist
    return dinamic_cryptolist


# get data cryptorates
async def get_top_cryptorates():
    dinamic_cryptolist = parse_top_cryptorates()
    crates = await get_cryptorates(dinamic_cryptolist)

    return crates
