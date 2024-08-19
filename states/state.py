from aiogram.fsm.state import StatesGroup, State


class GetDates(StatesGroup):
    date1 = State()
    date2 = State()
