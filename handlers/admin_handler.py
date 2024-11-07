from aiogram import Router, F, types
from create_bot import pg_manager
from decouple import config


admin_router = Router()
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]


def is_admin(user_id):
    return user_id in admins


@admin_router.message(F.text == "/send_table_users")
async def send_table_users_handler(message: types.Message):
    print(message.from_user.id)
    print(is_admin(message.from_user.id))
    if is_admin(message.from_user.id):
        await message.answer("Это админская команда!")
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


@admin_router.message(F.text == "/send_table_records")
async def send_table_records_handler(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer("Это админская команда!")
        await pg_manager.connect()
        try:
            user_data = await pg_manager.get_both_tables()
            headers = ["Records", "full_name", "object", "system", "hours", "notes"]
            column_widths = [20, 8, 50, 17]
            header_row = (
                f"{headers[0].ljust(column_widths[1])}"
                f"{headers[1].ljust(column_widths[0])}"
                f"{headers[2].ljust(column_widths[0])}"
                f"{headers[3].ljust(column_widths[3])}"
                f"{headers[4].ljust(column_widths[1])}"
                f"{headers[5].ljust(column_widths[2])}"
            )

            formatted_rows = [
                f"{str(record['full_name']).ljust(column_widths[0])}"
                f"{str(record['object']).ljust(column_widths[0])}"
                f"{str(record['system']).ljust(column_widths[0])}"
                f"{str(record['spent_time']).ljust(column_widths[1])}"
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
