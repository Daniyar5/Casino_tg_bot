from aiogram.fsm.state import State, StatesGroup

class UserForm(StatesGroup):
    name = State()
    age = State()
    email = State()

class DepositForm(StatesGroup):
    card_number = State()
    expiry = State()
    cvv = State()
    amount = State()