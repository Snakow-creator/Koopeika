from core.exceptions import ProfileExpiredError
from tasks.logger import log

from time import time

class Profile:
    _storage = {}

    def __init__(self, user_id: int):
        self.tg_id: int = user_id
        self.choise: str = None
        self.con_choise: str = None
        self.check: str = None
        self.text: str = None
        self.value: str = None
        self.amount: int = 0
        self.con_value: str = None
        self.transactions = None
        self.transactions_page: int = 1
        self.trs_edit_page: int = 1
        self.tr_message_id: str = None
        self.assets_balance: dict = {}
        self.assets_share: dict = {}
        self.last_activity = time() # save time of create object

        Profile._storage[self.tg_id] = self


    @classmethod
    def get(cls, user_id, create=False):
        user = cls._storage.get(user_id)

        if user is None:
            if create:
                user = cls(user_id)
            else:
                raise ProfileExpiredError()

        user.last_activity = time() # save time of change object
        return user

    # clear unactive user sessions
    @classmethod
    def cleanup(cls, timeout=3600):
        log.debug("check unactive profiles")
        now = time()

        expired = [
            user_id
            for user_id, profile in cls._storage.items()
            if now - profile.last_activity > timeout
        ]

        for user_id in expired:
            del cls._storage[user_id]
