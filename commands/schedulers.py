from operations.rates import get_exchange_rates, cryptorates
from loggers.logs import log

import database.online_config as oc


def const_rates():
    oc.rates = get_exchange_rates()


async def dinamic_cryptorates():
    oc.cryptorates = await cryptorates()
    log.debug(f"Get dinamic cryptorates\n" f"{oc.cryptorates}")
