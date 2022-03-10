from aiogram.dispatcher.filters.state import State, StatesGroup


class ReceiptStates(StatesGroup):
    confirm = State()