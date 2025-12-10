from aiogram.fsm.state import State, StatesGroup


class BalanceState(StatesGroup):
    change = State()
    assets_end = State()
    input_crypto = State()
