from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    registration = State()
    msg_for_all = State()
    subscribe = State()
    change_name = State()
    unsubscribe = State()