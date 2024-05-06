from aiogram.fsm.state import State, StatesGroup

class CalculatorFillForm(StatesGroup):
    fill_number = State()
    fill_name = State()
    fill_product = State()
    fill_length = State()
    fill_width = State()
    fill_depth = State()
    fill_underframe = State()
    fill_request = State()