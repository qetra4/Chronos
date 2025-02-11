from aiogram import Router, types
from decouple import config
from keyboards import *


admin_router = Router()
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]


def is_admin(user_id):
    return user_id in admins


async def send_table_users(message: types.Message):
    if is_admin(message.from_user.id):
        await pg_manager.connect()
        try:
            user_data = await pg_manager.get_table('users')
            headers = ["Users", "user_id", "full_name", "role"]
            column_widths = [12, 25, 20, 6]

            header_row = (
                f"{headers[0].ljust(column_widths[3])}"
                f"{headers[1].ljust(column_widths[0])}"
                f"{headers[2].ljust(column_widths[1])}"
                f"{headers[3].ljust(column_widths[2])}"
            )

            formatted_rows = [
                f"{str(record['user_id']).ljust(column_widths[0])}"
                f"{str(record['full_name']).ljust(column_widths[1])}"
                f"{str(record['role']).ljust(column_widths[2])}"
                for record in user_data
            ]

            formatted_data = "\n".join([header_row] + formatted_rows)
            await message.answer(f"Данные таблицы users:\n\n```{formatted_data}```", parse_mode="Markdown")

        except Exception as e:
            await message.answer(f"Ошибка при получении данных таблицы: {e}")
        finally:
            await pg_manager.close()
    else:
        await message.answer("Недостаточно прав.")


async def send_table_records(message: types.Message):
    if is_admin(message.from_user.id):
        await pg_manager.connect()
        try:
            user_data = await pg_manager.get_users_and_records_tables()
            headers = ["Records", "full_name", "object", "system", "subsystem", "spent_time", "work_type", "date"]
            column_widths = [20, 8, 50, 25]
            header_row = (
                f"{headers[0].ljust(column_widths[1])}"
                f"{headers[1].ljust(column_widths[3])}"
                f"{headers[2].ljust(column_widths[0])}"
                f"{headers[3].ljust(column_widths[3])}"
                f"{headers[4].ljust(column_widths[0])}"
                f"{headers[5].ljust(column_widths[0])}"
                f"{headers[6].ljust(column_widths[0])}"
                f"{headers[7].ljust(column_widths[2])}"
            )

            formatted_rows = [
                f"{str(record['full_name']).ljust(column_widths[3])}"
                f"{str(record['object']).ljust(column_widths[0])}"
                f"{str(record['system']).ljust(column_widths[3])}"
                f"{str(record['subsystem']).ljust(column_widths[0])}"
                f"{str(record['spent_time']).ljust(column_widths[0])}"
                f"{str(record['work_type']).ljust(column_widths[0])}"
                f"{str(record['date']).ljust(column_widths[0])}"
                f"{str(record['notes']).ljust(column_widths[2])}"
                for record in user_data
            ]
            formatted_data = "\n".join([header_row] + formatted_rows)
            await message.answer(f"Данные таблицы records:\n\n```{formatted_data}```", parse_mode="Markdown")

        except Exception as e:
            await message.answer(f"Ошибка при получении данных таблицы: {e}")
        finally:
            await pg_manager.close()
    else:
        await message.answer("Недостаточно прав.")


async def send_table_banned_users(message: types.Message):
    if is_admin(message.from_user.id):
        await pg_manager.connect()
        try:
            user_data = await pg_manager.get_table('banned_users')
            headers = ["Banned_Users", "user_id"]
            column_widths = [12, 25, 20, 15]

            header_row = (
                f"{headers[0].ljust(column_widths[3])}"
                f"{headers[1].ljust(column_widths[0])}"
            )

            formatted_rows = [
                f"{str(record['user_id']).ljust(column_widths[0])}"
                for record in user_data
            ]

            formatted_data = "\n".join([header_row] + formatted_rows)
            await message.answer(f"Данные таблицы users:\n\n```{formatted_data}```", parse_mode="Markdown")

        except Exception as e:
            await message.answer(f"Ошибка при получении данных таблицы: {e}")
        finally:
            await pg_manager.close()
    else:
        await message.answer("Недостаточно прав.")


async def send_table_notifications(message: types.Message):
    if is_admin(message.from_user.id):
        await pg_manager.connect()
        try:
            user_data = await pg_manager.get_users_and_notifications_tables()
            headers = ["Notifications   ", "full_name", "hour", "minutes"]
            column_widths = [10, 20, 5, 16]

            header_row = (
                f"{headers[0].ljust(column_widths[2])}"
                f"{headers[1].ljust(column_widths[3])}"
                f"{headers[2].ljust(column_widths[0])}"
                f"{headers[3].ljust(column_widths[0])}"
            )

            formatted_rows = [
                f"{str(record['full_name']).ljust(column_widths[1])}"
                f"{str(record['hour']).ljust(column_widths[0])}"
                f"{str(record['minutes']).ljust(column_widths[0])}"
                for record in user_data
            ]

            formatted_data = "\n".join([header_row] + formatted_rows)
            await message.answer(f"Данные таблицы users:\n\n```{formatted_data}```", parse_mode="Markdown")

        except Exception as e:
            await message.answer(f"Ошибка при получении данных таблицы: {e}")
        finally:
            await pg_manager.close()
    else:
        await message.answer("Недостаточно прав.")


async def send_table_objects(message: types.Message):
    if is_admin(message.from_user.id):
        await pg_manager.connect()
        try:
            user_data = await pg_manager.get_table('objects')
            headers = ["Objects"]
            column_widths = [12, 25, 20, 15]

            header_row = (
                f"{headers[0].ljust(column_widths[3])}"
            )

            formatted_rows = [
                f"{str(record['object_name']).ljust(column_widths[0])}"
                for record in user_data
            ]

            formatted_data = "\n".join([header_row] + formatted_rows)
            await message.answer(f"Данные таблицы objects:\n\n```{formatted_data}```", parse_mode="Markdown")

        except Exception as e:
            await message.answer(f"Ошибка при получении данных таблицы: {e}")
        finally:
            await pg_manager.close()
    else:
        await message.answer("Недостаточно прав.")


async def send_table_systems(message: types.Message):
    if is_admin(message.from_user.id):
        await pg_manager.connect()
        try:
            user_data = await pg_manager.get_table('systems')
            headers = ["Systems"]
            column_widths = [12, 25, 20, 15]

            header_row = (
                f"{headers[0].ljust(column_widths[3])}"
            )

            formatted_rows = [
                f"{str(record['system_name']).ljust(column_widths[0])}"
                for record in user_data
            ]

            formatted_data = "\n".join([header_row] + formatted_rows)
            await message.answer(f"Данные таблицы systems:\n\n```{formatted_data}```", parse_mode="Markdown")

        except Exception as e:
            await message.answer(f"Ошибка при получении данных таблицы: {e}")
        finally:
            await pg_manager.close()
    else:
        await message.answer("Недостаточно прав.")


async def send_table_subsystems(message: types.Message):
    if is_admin(message.from_user.id):
        await pg_manager.connect()
        try:
            user_data = await pg_manager.get_table('subsystems')
            headers = ["Subsystems"]
            column_widths = [12, 25, 20, 15]

            header_row = (
                f"{headers[0].ljust(column_widths[3])}"
            )

            formatted_rows = [
                f"{str(record['subsystem_name']).ljust(column_widths[0])}"
                for record in user_data
            ]

            formatted_data = "\n".join([header_row] + formatted_rows)
            await message.answer(f"Данные таблицы subsystems:\n\n```{formatted_data}```", parse_mode="Markdown")

        except Exception as e:
            await message.answer(f"Ошибка при получении данных таблицы: {e}")
        finally:
            await pg_manager.close()
    else:
        await message.answer("Недостаточно прав.")


async def send_table_types_of_work(message: types.Message):
    if is_admin(message.from_user.id):
        await pg_manager.connect()
        try:
            user_data = await pg_manager.get_table('type_of_works')
            headers = ["Types_of_work"]
            column_widths = [12, 25, 20, 15]

            header_row = (
                f"{headers[0].ljust(column_widths[3])}"
            )

            formatted_rows = [
                f"{str(record['type_of_work_name']).ljust(column_widths[0])}"
                for record in user_data
            ]

            formatted_data = "\n".join([header_row] + formatted_rows)
            await message.answer(f"Данные таблицы type of works:\n\n```{formatted_data}```", parse_mode="Markdown")

        except Exception as e:
            await message.answer(f"Ошибка при получении данных таблицы: {e}")
        finally:
            await pg_manager.close()
    else:
        await message.answer("Недостаточно прав.")
