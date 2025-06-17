import database.requests as rq
import database.online_config as oc

from database.errors_config import BadMessageText, BadUserIdError, BigNumError
from operations.json_XML import get_exchange_rates
from operations.crypto_conversion import get_cryptorates

def const_rates():
    oc.rates = get_exchange_rates()


def const_cryptorates():
    oc.cryptorates = get_cryptorates()


async def checker_id(tg_id, delete_id):
    list_id = []
    list_transactions = await rq.Transactions.history_transactions(tg_id)
    for transaction in list_transactions:
        list_id.append(transaction.id)
    if delete_id in list_id:
        return
    raise BadUserIdError(delete_id)


async def checker_num(num: str, value: str):
    try:
        float(num) # check num to float

        max_num = oc.max_nun_values[value]
        if float(num) > max_num:
            raise BigNumError()

    except ValueError: # if float raise ValueError
        raise BadMessageText()
