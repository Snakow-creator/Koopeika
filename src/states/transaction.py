from aiogram.fsm.state import State, StatesGroup


class TransactionState(StatesGroup):
    edit = State()
    edit_end = State()
    delete = State()
