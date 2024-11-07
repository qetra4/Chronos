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
