import requests

from secret.config import cryptolist


def get_cryptorate(currency):
    pair = f"{currency}".upper()
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        if "price" in data:
            price = data["price"]
        return float(price)


def get_cryptorates():
    crates = {}
    global cryptolist
    for crypto in cryptolist:
        res = get_cryptorate(crypto)
        crates[crypto] = res
    return crates
