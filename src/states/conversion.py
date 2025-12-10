from aiogram.fsm.state import State, StatesGroup


class ConversionState(StatesGroup):
    input_number = State()
    input_crypto = State()
