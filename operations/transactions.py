from datetime import datetime
from zoneinfo import ZoneInfo

import database.online_config as oc
import database.requests as rq


# Получение времени
async def format_time(unformatted_time: datetime, timezone: str):
    time = datetime.strptime(unformatted_time, "%Y-%m-%d %H:%M")
    time = time.astimezone(ZoneInfo(oc.tz_map[timezone]))
    formatted_time = time.strftime("%Y-%m-%d %H:%M")
    dt = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M")
    formatted_time = f"{dt.day} {oc.months[dt.month]} {dt.strftime('%H:%M')}"

    return formatted_time


# функция получения текста транзакции для callback и message
async def get_history_transactions(user_id):
    user = await rq.user_get(user_id)
    timezone, style = user.time_zone, user.style
    list_transactions = []
    text = "<b>История тразнакций:</b>\n"
    text_transactions = await rq.Transactions.history_transactions(user_id)

    for index, info in enumerate(text_transactions, start=1):
        time = await format_time(info.time, timezone)
        num_id, amount, value = info.id, info.amount, info.value
        description = info.description
        emoji = "🟩" if amount[0] == "+" else "🟥"
        if description:
            text += (
                f"{index}.{emoji} <b>{time}</b>"
                f"\n<b>{amount} {oc.values_symbols[style][value]}</b>({description})"
                f"\nid: <code>{num_id}</code>\n\n"
            )
        else:
            text += (
                f"{index}.{emoji} <b>{time}</b>"
                f"\n<b>{amount} {oc.values_symbols[style][value]}</b>"
                f"\nid: <code>{num_id}</code>\n\n"
            )
        if (index % 10) == 0:
            list_transactions.append(text)
            text = ""

    if text:
        list_transactions.append(text)
    oc.data_user_transactions[user_id] = list_transactions

    return list_transactions
