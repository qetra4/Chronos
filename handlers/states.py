# handlers/states.py
from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_role = State()
    waiting_for_object = State()
    waiting_for_system = State()
    waiting_for_spent_time = State()
    waiting_for_notes = State()
    waiting_for_more = State()
