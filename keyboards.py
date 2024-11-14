from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import admins


def role_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="📝 Программист"), KeyboardButton(text="👤 Монтажник")],
        [KeyboardButton(text="📖 Руководитель проекта")]
    ]
#    if user_telegram_id in admins:
#        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def yes_no_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def tell_info_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Да, расскажу"), KeyboardButton(text="Нет, в другой раз")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def objects_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Мостман"), KeyboardButton(text="Сосновка"), KeyboardButton(text="Парк Тауер")],
        [KeyboardButton(text="Пестово_33"), KeyboardButton(text="Офис"), KeyboardButton(text="Life_244")],
        [KeyboardButton(text="Кутузовский"), KeyboardButton(text="Технониколь_Рязань")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def systems_kb(user_telegram_id: int):
    kb_list = [
         [KeyboardButton(text="СВН - Видеонаблюдение"), KeyboardButton(text="АУД - Умный дом")],
         [KeyboardButton(text="СКС - Слаботочные сети"), KeyboardButton(text=" АВ - Аудио/Видео")],
         [KeyboardButton(text="ДМС - Домофонные системы"), KeyboardButton(text="ЭОМ - Электрика")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def subsystems_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Освещение"), KeyboardButton(text="Климат-контроль"),KeyboardButton(text="Шторы")],
        [KeyboardButton(text="Инженерные системы"),KeyboardButton(text="Теплый пол"), KeyboardButton(text="Протечки")],
        [KeyboardButton(text="Управление"), KeyboardButton(text="Интерфейс"),KeyboardButton(text="Голосовое управление")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def types_of_work_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Подключение щита"), KeyboardButton(text="Монтаж")],
        [KeyboardButton(text="Кабельные работы"), KeyboardButton(text="Проектирование")],
        [KeyboardButton(text="Сборка щита"), KeyboardButton(text="Программирование")],
        [KeyboardButton(text="Обследование")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
