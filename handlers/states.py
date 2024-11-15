from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_role = State()
    waiting_for_object = State()
    waiting_for_system = State()
    waiting_for_subsystem = State()
    waiting_for_type_of_work = State()
    waiting_for_spent_time = State()
    waiting_for_notes = State()
    waiting_for_more = State()
    waiting_for_password = State()
    waiting_for_info = State()
    waiting_for_notification_chose = State()
    waiting_for_hour = State()
    waiting_for_minute = State()
