from datetime import datetime
from zoneinfo import ZoneInfo
from database.errors_config import PageError

import database.online_config as oc
import database.requests as rq


class ListTransactions:
    def __init__(self, tg_id, list_transactions):
        self.tg_id = tg_id
        self.list_transactions = list_transactions

        profile = oc.Profile.get(tg_id)
        profile.transactions = self
        profile.transactions_page = 1

    @classmethod
    async def load(cls, tg_id):
        transactions_obj = await rq.Transactions.load(tg_id)
        transactions = transactions_obj.transactions
        user_obj = await rq.SelectUser.load(tg_id)
        user = user_obj.user

        list_transactions = {}
        text = "<b>История транзакций:</b>\n"
        for ind, tr in enumerate(transactions, start=1):
            time = await cls._format_time(tr["time"], user["time_zone"])
            emoji = "🟩" if tr["amount"][0] == "+" else "🟥"

            if tr["description"]:
                second_line = f"\n<b>{tr["amount"]}{oc.values_symbols[user["style"]].get(tr["value"], f' {tr["value"]}')}</b>({tr["description"]})"
            else:
                second_line = (
                    f"\n<b>{tr["amount"]}{oc.values_symbols[user["style"]].get(tr["value"], f' {tr["value"]}')}</b>"
                )

            text += f"{ind}.{emoji} <b>{time}</b>" f"{second_line}" f"\nid: <code>{tr["id"]}</code>\n\n"
            if ind % 10 == 0:
                list_transactions[ind / 10] = text
                text = "<b>История транзакций:</b>\n"

        if text != "<b>История транзакций:</b>\n":
            len_pages = len(list_transactions)
            list_transactions[len_pages + 1] = text

        return cls(tg_id, list_transactions)

    def get(self):
        return self.list_transactions.get(1)

    async def page(self, page: int):
        if page in self.list_transactions.keys():
            profile = oc.Profile.get(self.tg_id)
            profile.transactions_page = page
            return self.list_transactions.get(page)
        raise PageError

    def pages(self):
        return len(self.list_transactions)

    @staticmethod
    async def _format_time(unformatted_time: datetime, timezone: str):
        time = datetime.strptime(unformatted_time, "%Y-%m-%d %H:%M")
        time = time.astimezone(ZoneInfo(oc.tz_map[timezone]))
        formatted_time = time.strftime("%Y-%m-%d %H:%M")
        dt = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M")
        formatted_time = f"{dt.day} {oc.months[dt.month]} {dt.strftime('%H:%M')}"

        return formatted_time
