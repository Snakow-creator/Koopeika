from operations.rates import get_exchange_rates, get_cryptorates

import database.online_config as oc


def const_rates():
    oc.rates = get_exchange_rates()


def const_cryptorates():
    oc.cryptorates = get_cryptorates()
