from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import pg_manager


def role_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="📝 Программист"), KeyboardButton(text="👤 Монтажник")],
        [KeyboardButton(text="📖 Руководитель проекта")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def yes_no_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def yes_no_know_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")],
        [KeyboardButton(text="Не знаю")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def tell_info_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Да, расскажу"), KeyboardButton(text="Нет, в другой раз")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def period_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Вчера"), KeyboardButton(text="Завтра")],
        [KeyboardButton(text="За выбранную мной дату")],
        [KeyboardButton(text="По выбранный мной день включительно")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


async def objects_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    await pg_manager.connect()
    try:
        rows = await pg_manager.get_object_data()
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


async def user_objects_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
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


async def left_objects_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    await pg_manager.connect()
    try:
        user_rows = await pg_manager.get_keyboard_data(user_id=user_telegram_id)
        user_objects = [row["object_name"] for row in user_rows]
        common_rows = await pg_manager.get_object_data()
        common_objects = [row["object_name"] for row in common_rows]
        left_objects = [obj for obj in common_objects if obj not in user_objects]
        kb_list = [
            [KeyboardButton(text=left_objects[i]), KeyboardButton(text=left_objects[i + 1])]
            if i + 1 < len(left_objects) else [KeyboardButton(text=left_objects[i])]
            for i in range(0, len(left_objects), 2)
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
        return keyboard
    except Exception as e:
        print(f"Ошибка при создании клавиатуры: {e}")
        return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    finally:
        await pg_manager.close()


async def m_systems_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
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


async def c_systems_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    await pg_manager.connect()
    try:
        rows = await pg_manager.get_table("c_systems")
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


async def systems_coder_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="Освещение"), KeyboardButton(text="Теплые полы")],
        [KeyboardButton(text="Видеонаблюдение"), KeyboardButton(text="Шторы")],
        [KeyboardButton(text="Домофония"), KeyboardButton(text="Протечки")],
        [KeyboardButton(text="Мультимедия"), KeyboardButton(text="Климат")],
        [KeyboardButton(text="Прочее (указать свое)")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


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


async def m_types_of_work_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
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


async def c_types_of_work_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    await pg_manager.connect()
    try:
        rows = await pg_manager.get_table("c_type_of_works")
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


async def types_of_work_coder_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="Программирование"), KeyboardButton(text="Пусконаладка")],
        [KeyboardButton(text="Разработка Интерфейса"), KeyboardButton(text="Тестирование")],
        [KeyboardButton(text="Прочее (указать свое)")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def admin_choose_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Отобрази таблицу"), KeyboardButton(text="Покажи график")],
        [KeyboardButton(text="Открой keyboards-редактор")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def admin_choose_m_kb_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Объекты"), KeyboardButton(text="Системы")],
        [KeyboardButton(text="Подсистемы"), KeyboardButton(text="Тип работы")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def admin_choose_c_kb_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Объекты"), KeyboardButton(text="Системы")],
        [KeyboardButton(text="Тип работы")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def admin_whom_edit_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Программистам"), KeyboardButton(text="Монтажникам")]
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


def choose_table_to_show_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Круговая диаграмма часов работы extra/not extra")],
        [KeyboardButton(text="Гистограмма часов работы по объектам")],
        [KeyboardButton(text="Гистограмма часов работы по системам")],
        [KeyboardButton(text="Гистограмма часов работы по подсистемам")],
        [KeyboardButton(text="Гистограмма часов работы по типам работ")],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
