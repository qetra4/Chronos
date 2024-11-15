from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from handlers.states import RegistrationStates
from create_bot import pg_manager
from decouple import config
from messages import MESSAGES
from keyboards import *


admin_router = Router()
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]


def is_admin(user_id):
    return user_id in admins


@admin_router.message(F.text == "/admin")
async def admin_handler(message: types.Message, state: FSMContext):
    await pg_manager.connect()
    is_user_banned = await pg_manager.is_user_banned(user_id=message.from_user.id)
    if not is_user_banned:
        if is_admin(message.from_user.id):
            await message.answer(MESSAGES["admin_choose_option"], reply_markup=admin_choose_kb(message.from_user.id))
            await state.set_state(RegistrationStates.waiting_for_admin_chose)
        else:
            await message.answer("Недостаточно прав.")
    await pg_manager.close()


@admin_router.message(RegistrationStates.waiting_for_admin_chose)
async def admin_choose_handler(message: types.Message, state: FSMContext):
    admin_info = message.text
    await state.update_data(admin_info=admin_info)
    if admin_info == 'Отобрази таблицу':
        await message.answer(MESSAGES['admin_choose_table'], reply_markup=admin_choose_table_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_admin_table)
    elif admin_info == 'Покажи график':
        await message.answer(MESSAGES['why_not'], reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.waiting_for_admin_diagram)


@admin_router.message(RegistrationStates.waiting_for_admin_table)
async def admin_choose_table_handler(message: types.Message, state: FSMContext):
    admin_table = message.text
    await state.update_data(admin_info=admin_table)
    if admin_table == 'Таблица Users':
        await send_table_users_handler(message)
    elif admin_table == 'Таблица Records':
        await send_table_records_handler(message)
#   elif admin_info == 'Таблица Banned Users':
#
#   elif admin_info == 'Таблица Notifications':
#


@admin_router.message(RegistrationStates.send_table_users)
async def send_table_users_handler(message: types.Message):
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


@admin_router.message(RegistrationStates.send_table_records)
async def send_table_records_handler(message: types.Message):
    if is_admin(message.from_user.id):
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
