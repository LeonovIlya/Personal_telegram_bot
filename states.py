from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    auth = State()
    ai = State()
    voice = State()
    reminder = State()
    reminder_add = State()
