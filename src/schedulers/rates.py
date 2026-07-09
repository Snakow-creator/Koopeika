from tasks.logger import log
from config import conf

from rates.rates import get_exchange_rates
from rates.cryptorates import get_top_cryptorates




def const_rates():
    conf.rates = get_exchange_rates()
    log.debug(f"Get exchange cryptorates")


async def dinamic_cryptorates():
    conf.cryptorates = await get_top_cryptorates()
    log.debug(f"Get dinamic cryptorates")
