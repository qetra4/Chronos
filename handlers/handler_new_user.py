from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import RegistrationStates
from messages import MESSAGES
from keyboards import *
from decouple import config
from datetime import datetime


new_user_router = Router()


@new_user_router.message(F.text == "/start")
async def start_command_handler(message: Message, state: FSMContext):
    await pg_manager.connect()
    is_user_banned = await pg_manager.is_user_banned(user_id=message.from_user.id)
    if not is_user_banned:
        user_info = await pg_manager.get_user_data(user_id=message.from_user.id, table_name='users')
        if user_info:
            user_role = await pg_manager.get_user_role(user_id=message.from_user.id, table_name='users')
            await state.update_data(user_role=user_role)
            await message.answer(MESSAGES['hello'])
            await message.answer(MESSAGES['intention_message'], reply_markup=tell_info_kb(message.from_user.id))
            if str(user_role) == "<Record role='📝 Программист'>":
                await state.set_state(RegistrationStates.waiting_for_info_coder)
            else:
                await state.set_state(RegistrationStates.waiting_for_info_mounter)
            date_fill = (datetime.now().strftime('%d-%m-%Y'))
            date_fill = datetime.strptime(date_fill, '%d-%m-%Y').date()
            await state.update_data(user_date=date_fill)
        else:
            await message.answer(MESSAGES['user_pass'])
            await state.set_state(RegistrationStates.waiting_for_password)
    await pg_manager.close()


@new_user_router.message(RegistrationStates.waiting_for_password)
async def get_password_handler(message: types.Message, state: FSMContext):
    user_pass = message.text
    data = await state.get_data()
    number_of_tries = data.get("number_of_tries", 0)

    if user_pass == config('USER_PASS'):
        await message.answer(MESSAGES['know_name'])
        await state.set_state(RegistrationStates.waiting_for_name)
    else:
        number_of_tries += 1
        await state.update_data(number_of_tries=number_of_tries)
        if number_of_tries >= 3:
            await pg_manager.connect()
            await pg_manager.create_ban_table()
            await pg_manager.ban_user(user_id=message.from_user.id)
            await message.answer(MESSAGES['banned_message'])
            await state.clear()
            await pg_manager.close()
        else:
            await message.answer(MESSAGES['wrong_answer'])


@new_user_router.message(RegistrationStates.waiting_for_name)
async def get_name_handler(message: Message, state: FSMContext):
    user_name = message.text
    await state.update_data(user_name=user_name)
    await message.answer(MESSAGES['know_role'],
                         reply_markup=role_kb(message.from_user.id))
    await state.set_state(RegistrationStates.waiting_for_role)


@new_user_router.message(RegistrationStates.waiting_for_role)
async def get_role_handler(message: Message, state: FSMContext):
    user_role = message.text
    user_data = await state.get_data()
    user_name = user_data.get('user_name')
    user_id = message.from_user.id
    await pg_manager.connect()
    if user_name is None:
        await message.answer("Произошла ошибка: не удалось получить имя пользователя.")
        await state.clear()
        return

    if user_id is None:
        await message.answer("Произошла ошибка: не удалось получить идентификатор пользователя.")
        await state.clear()
        return

    await pg_manager.create_table_users()
    await pg_manager.create_user_keyboard_table()
    all_objects = await pg_manager.get_object_names()

    try:
        await pg_manager.insert_data(
            table_name="users",
            records_data={
                "user_id": user_id,
                "full_name": user_name,
                "role": user_role
            }
        )
    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении данных: {e}")
        await state.clear()

    try:
        for obj in all_objects:
            await pg_manager.insert_data(
                table_name="user_keyboard",
                records_data={
                    "user_id": user_id,
                    "object_name": obj['object_name'],
                }
            )
        await message.answer(f"Спасибо, {user_name}! Твоя роль '{user_role}' сохранена.")
        keyboard = await objects_kb(message.from_user.id)
        await message.answer(MESSAGES['know_object'], reply_markup=keyboard)
        today = datetime.now().date()
        await state.update_data(user_date=today)
        if str(user_role) == "<Record role='📝 Программист'>":
            await state.set_state(RegistrationStates.waiting_for_object_coder)
        else:
            await state.set_state(RegistrationStates.waiting_for_object_mounter)
    except Exception as e:
        await message.answer(f"Произошла ошибка при создании object keyboard {e}")
        await state.clear()

    await pg_manager.close()
