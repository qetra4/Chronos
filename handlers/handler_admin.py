from aiogram import F
from aiogram.fsm.context import FSMContext
from handlers.states import RegistrationStates
from messages import MESSAGES
from funcs_admin import *


admin_router = Router()
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]


def is_admin(user_id):
    return user_id in admins


@admin_router.message(F.text == "/admin")
async def admin_handler(message: types.Message, state: FSMContext):
    await pg_manager.connect()
    is_user_banned = await pg_manager.is_user_banned(user_id=message.from_user.id)
    if not is_user_banned:
        user_info = await pg_manager.get_user_data(user_id=message.from_user.id, table_name='users')
        if user_info:
            if is_admin(message.from_user.id):
                await message.answer(MESSAGES["admin_choose_option"], reply_markup=admin_choose_kb(message.from_user.id))
                await state.set_state(RegistrationStates.waiting_for_admin_chose)
            else:
                await message.answer("Недостаточно прав.")
        else:
            await message.answer(MESSAGES['user_pass'])
            await state.set_state(RegistrationStates.waiting_for_password)
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
    elif admin_table == 'Таблица Banned Users':
        await send_table_banned_users_handler(message)
    elif admin_table == 'Таблица Notifications':
        await send_table_notifications_handler(message)

