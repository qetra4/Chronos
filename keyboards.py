from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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

