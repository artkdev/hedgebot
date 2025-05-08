from aiogram.fsm.state import State, StatesGroup

class HedgeStates(StatesGroup):
    type = State()
    pair = State()
    amount = State()
