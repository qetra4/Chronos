from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import admins, pg_manager


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


async def objects_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    await pg_manager.connect()
    try:
        rows = await pg_manager.get_keyboard_data(user_id=user_telegram_id)
        objects = [row["object_name"] for row in rows]
        kb_list = [
            [KeyboardButton(text=objects[i]), KeyboardButton(text=objects[i + 1])]
            if i + 1 < len(objects) else [KeyboardButton(text=objects[i])]
            for i in range(0, len(objects), 2)
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
        return keyboard
    except Exception as e:
        print(f"Ошибка при создании клавиатуры: {e}")
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    finally:
        await pg_manager.close()


async def systems_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    await pg_manager.connect()
    try:
        rows = await pg_manager.get_table("systems")
        objects = [row["system_name"] for row in rows]
        kb_list = [
            [KeyboardButton(text=objects[i]), KeyboardButton(text=objects[i + 1])]
            if i + 1 < len(objects) else [KeyboardButton(text=objects[i])]
            for i in range(0, len(objects), 2)
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
        return keyboard
    except Exception as e:
        print(f"Ошибка при создании клавиатуры: {e}")
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    finally:
        await pg_manager.close()


async def subsystems_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    await pg_manager.connect()
    try:
        rows = await pg_manager.get_table("subsystems")
        objects = [row["subsystem_name"] for row in rows]
        kb_list = [
            [KeyboardButton(text=objects[i]), KeyboardButton(text=objects[i + 1])]
            if i + 1 < len(objects) else [KeyboardButton(text=objects[i])]
            for i in range(0, len(objects), 2)
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
        return keyboard
    except Exception as e:
        print(f"Ошибка при создании клавиатуры: {e}")
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    finally:
        await pg_manager.close()


async def types_of_work_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    await pg_manager.connect()
    try:
        rows = await pg_manager.get_table("type_of_works")
        objects = [row["type_of_work_name"] for row in rows]
        kb_list = [
            [KeyboardButton(text=objects[i]), KeyboardButton(text=objects[i + 1])]
            if i + 1 < len(objects) else [KeyboardButton(text=objects[i])]
            for i in range(0, len(objects), 2)
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
        return keyboard
    except Exception as e:
        print(f"Ошибка при создании клавиатуры: {e}")
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    finally:
        await pg_manager.close()


def admin_choose_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Отобрази таблицу"), KeyboardButton(text="Покажи график")],
        [KeyboardButton(text="Открой keyboards-редактор")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def admin_choose_kb_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Объекты"), KeyboardButton(text="Системы")],
        [KeyboardButton(text="Подсистемы"), KeyboardButton(text="Тип работы")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def admin_way_to_edit_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Создать кнопку"), KeyboardButton(text="Удалить кнопку")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def admin_choose_table_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Таблица Users"), KeyboardButton(text="Таблица Records")],
        [KeyboardButton(text="Таблица Banned Users"), KeyboardButton(text="Таблица Notifications")],
        [KeyboardButton(text="Таблица Types_of_work"), KeyboardButton(text="Таблица Objects")],
        [KeyboardButton(text="Таблица Systems"), KeyboardButton(text="Таблица Subsystems")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def user_obj_what_to_do(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Добавить кнопку"), KeyboardButton(text="Удалить кнопку")],
        [KeyboardButton(text="Отобразить текущую клавиатуру")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
