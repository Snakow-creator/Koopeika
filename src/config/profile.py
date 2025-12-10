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
        self.tr_message_id: str = None
        self.assets_balance: dict = {}
        self.assets_share: dict = {}

        Profile._storage[self.tg_id] = self

    @classmethod
    def get(cls, user_id):
        user = cls._storage.get(user_id)
        if not user:
            user = cls(user_id)
        return user
