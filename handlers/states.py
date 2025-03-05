from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    # Авторизация
    waiting_for_name = State()
    waiting_for_role = State()
    waiting_for_password = State()

    # Настройка уведомлений
    waiting_for_notification_chose = State()
    waiting_for_hour = State()
    waiting_for_minute= State()

    # Панель администратора
    waiting_for_admin_chose = State()
    waiting_for_admin_table = State()
    waiting_for_admin_diagram = State()
    waiting_for_admin_keyboard_choose = State()
    waiting_for_admin_to_whom_edit_keyboard = State()
    waiting_for_graphic_chose = State()
    waiting_for_way_to_edit_keyboard = State()
    waiting_for_obj_what_to_do = State()
    waiting_for_create_button = State()
    waiting_for_delete_button = State()

    # Изменения в клавиатуре пользователем
    waiting_for_tap_to_hide_keyboard = State()
    waiting_for_tap_to_add_button = State()
    waiting_for_tap_to_delete_button = State()
    
    # Сбор информации у программистов
    waiting_for_object_coder = State()
    waiting_for_system_coder = State()
    waiting_for_subsystem_coder = State()
    waiting_for_type_of_work_coder = State()
    waiting_for_spent_time_coder = State()
    waiting_for_notes_coder = State()
    waiting_for_more_coder = State()
    waiting_for_info_coder = State()
    waiting_for_extra_coder = State()
    waiting_for_period_coder = State()
    waiting_for_date_coder = State()
    waiting_for_date_period_coder = State()
    waiting_for_if_notes_coder = State()
    waiting_for_same_object_coder = State()
    waiting_for_his_own_system_coder = State()
    waiting_for_his_own_type_of_work_coder = State()

    # Сбор информации у монтажников
    waiting_for_object_mounter = State()
    waiting_for_system_mounter = State()
    waiting_for_subsystem_mounter = State()
    waiting_for_type_of_work_mounter = State()
    waiting_for_spent_time_mounter = State()
    waiting_for_notes_mounter = State()
    waiting_for_more_mounter = State()
    waiting_for_info_mounter = State()
    waiting_for_extra_mounter = State()
    waiting_for_period_mounter = State()
    waiting_for_date_mounter = State()
    waiting_for_date_period_mounter = State()
    waiting_for_if_notes_mounter = State()
    waiting_for_same_object_mounter = State()
