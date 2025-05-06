from aiogram.fsm.state import State, StatesGroup


# класс со статусами
class PromocodeFillForm(StatesGroup):
    fill_1 = State()
    fill_2 = State()
