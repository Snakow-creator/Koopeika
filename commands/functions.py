import database.requests as rq
import database.online_config as oc

from aiogram.types import Message

from database.errors_config import BadMessageText, BadUserIdError, BigNumError


async def message_update(message: Message, text, keyboard=None):
    if keyboard:
        oc.msg[message.from_user.id] = await message.answer(text, reply_markup=keyboard)
    else:
        oc.msg[message.from_user.id] = await message.answer(text)


async def delete_message(message: Message):
    msg = oc.msg.get(message.from_user.id)
    await message.delete()
    await msg.delete()


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


# convert to true num
async def convert_num(num: str, user_id: int) -> str:
    i = num.find(".")
    user = await rq.user_get(user_id)
    fiat_len, crypto_len = user.fiat_amount, user.crypto_amount
    # if num is rates currency
    if len(num[i+1:]) == 3:
        res = "{:,.{s}f}".format(float(num), s=fiat_len)
        return res
    # if num is crypto currency
    if len(num[i+1:]) == 9:
        res = "{:,.{s}f}".format(float(num), s=crypto_len)
        return res

