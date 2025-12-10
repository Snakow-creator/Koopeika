from core.exceptions import BadMessageText, BadUserIdError, BigNumError, ValueNotFoundError
from config import conf

from middlewares.logger import log


async def checker_id(changed_id, user_transactions):
    list_id = []
    for transaction in user_transactions:
        list_id.append(transaction["id"])
        if changed_id in list_id:
            return transaction["amount"][0]
    raise BadUserIdError()


async def checker_value(value: str):
    if value[-4:] in ("USDT", "USDC"):
        value = value[:-4]
    if not conf.cryptorates.get(value, False):
        raise ValueNotFoundError

    return value


async def checker_num(num: str, value: str, premium_user, con_type: bool = False):
    if con_type == True:
        max_limit = 1_000_000_000_000
    # if type is just assets
    else:
        max_limit = 1_000_000_000

    try:
        max_num = conf.max_num_values.get(value, max_limit)

        if premium_user:
            max_num = conf.max_num_values_premium.get(value, max_limit*1_000)
        if float(num) > max_num:
            raise BigNumError()

    except ValueError:  # if float raise ValueError
        raise BadMessageText()


async def int_or_float(num: str):
    # if . in str num
    if num.find(".") != -1:
        return float(num)

    return int(num)
