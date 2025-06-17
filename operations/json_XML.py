from secret.config import NBK_API

import requests

import xml.etree.ElementTree as ES


def get_exchange_rates():
    rates = {"KZT": 1}
    res = requests.get(NBK_API)
    res = res.text
    root = ES.fromstring(res)
    items = root.find("channel").findall("item")
    for item in items:
        rates[item.findtext("title")] = float(item.findtext("description"))
    return rates
