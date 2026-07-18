import requests

import xml.etree.ElementTree as ES

from config.secret import NBK_API
from tasks.logger import log


# country values
def get_exchange_rates():
    # get data API
    rates = {"KZT": 1}
    res = requests.get(NBK_API)
    res = res.text

    # parse data
    root = ES.fromstring(res)
    items = root.find("channel").findall("item")
    for item in items:
        rates[item.findtext("title")] = float(item.findtext("description"))

    log.debug(f"Get exchange rates")
    return rates
