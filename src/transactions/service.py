from datetime import datetime
from zoneinfo import ZoneInfo
from textwrap import shorten

from config import conf
from transactions.request import Transactions
from users import user_req

from core.exceptions import PageError
from config import profile

from tasks.logger import log


class ListTransactions:
    def __init__(self, tg_id, list_trs, trs):
        self.tg_id = tg_id
        self.list_transactions = list_trs
        self.transactions = trs

        prof = profile.get(tg_id, create=True)
        prof.transactions = self
        prof.transactions_page = 1

    @classmethod
    async def load(cls, tg_id):
        transactions_obj = await Transactions.load(tg_id)
        transactions = transactions_obj.transactions
        user_obj = await user_req.load(tg_id)
        user = user_obj.user

        list_transactions = {}
        text = "<b>История транзакций:</b>\n"
        for ind, tr in enumerate(transactions, start=1):
            time = await cls._format_time(tr["time"], user["time_zone"])
            emoji = "🟩" if tr["amount"][0] == "+" else "🟥"
            value = conf.values_symbols[user["style"]].get(
                tr["value"], f" {tr['value']}"
            )

            if tr["description"]:
                second_line = f"\n<b>{tr['amount']}{value}</b>({tr['description']})"
            else:
                second_line = f"\n<b>{tr['amount']}{value}</b>"

            text += (
                f"{ind}.{emoji} <b>{time}</b>"
                f"{second_line}"
                f"\nid: <code>{tr['id']}</code>\n\n"
            )
            if ind % 10 == 0:
                list_transactions[ind // 10] = text
                text = "<b>История транзакций:</b>\n"

        if text != "<b>История транзакций:</b>\n":
            len_pages = len(list_transactions)
            list_transactions[len_pages + 1] = text

        return cls(tg_id, list_transactions, transactions)

    def get(self):
        return self.list_transactions.get(1)

    async def page(self, page: int):
        if page in self.list_transactions.keys():
            prof = profile.get(self.tg_id)
            prof.transactions_page = page
            return self.list_transactions.get(page)
        raise PageError

    async def load_edit_kb(self):
        trs = self.transactions
        user_obj = await user_req.load(self.tg_id)
        user = user_obj.user

        prof = profile.get(self.tg_id)
        prof.trs_edit_page = 1

        buttons_trs = [[]]
        for ind, tr in enumerate(trs, start=1):
            emoji = "🟢" if tr["amount"][0] == "+" else "🔴"
            value = conf.values_symbols[user["style"]].get(
                tr["value"], f" {tr['value']}"
            )
            if tr["description"]:
                text = f"{emoji} {tr['id']}. {tr["amount"]}{value} ({tr['description']})"
            else:
                text = f"{emoji} {tr['id']}. {tr["amount"]}{value}"

            buttons_trs[-1].append((tr["id"], text))

            if ind % 10 == 0:
                buttons_trs.append([])

        self.list_edit_transactions = buttons_trs
        return buttons_trs[0]

    async def edit_page(self, page: int):
        if page in self.list_transactions.keys():
            prof = profile.get(self.tg_id)
            prof.trs_edit_page = page
            return self.list_edit_transactions[page - 1]
        raise PageError


    def pages(self):
        pages = len(self.list_transactions)
        if pages:
            return pages
        # if pages does not exist
        return -1

    def edit_pages(self):
        pages = len(self.list_edit_transactions)
        if pages:
            return pages
        # if pages does not exist
        return -1

    @staticmethod
    async def _format_time(unformatted_time: datetime, timezone: str):
        time = datetime.strptime(unformatted_time, "%Y-%m-%d %H:%M")
        time = time.astimezone(ZoneInfo(conf.tz_map[timezone]))
        formatted_time = time.strftime("%Y-%m-%d %H:%M")
        dt = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M")
        formatted_time = f"{dt.day} {conf.months[dt.month]} {dt.strftime('%H:%M')}"

        return formatted_time
