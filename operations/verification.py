from database.errors_config import BadMessageText, BadUserIdError, BigNumError

import database.online_config as oc


async def checker_id(delete_id, user_transactions):
    list_id = []
    for transaction in user_transactions:
        list_id.append(transaction.id)
    if delete_id in list_id:
        return
    raise BadUserIdError()


async def checker_num(num: str, value: str):
    try:
        float(num)  # check num to float

        max_num = oc.max_nun_values[value]
        if float(num) > max_num:
            raise BigNumError()

    except ValueError:  # if float raise ValueError
        raise BadMessageText()


async def checker_con_num(num: str, value: str):
    try:
        float(num)  # check num to float

        max_num = oc.max_con_values[value]
        if float(num) > max_num:
            raise BigNumError()

    except ValueError:  # if float raise ValueError
        raise BadMessageText()
