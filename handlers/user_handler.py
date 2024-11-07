from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from create_bot import pg_manager
from handlers.states import RegistrationStates
from messages import MESSAGES
from keyboards import *

user_router = Router()


@user_router.message(F.text == "/start")
async def start_command_handler(message: Message, state: FSMContext):
    await pg_manager.connect()
    user_info = await pg_manager.get_user_data(user_id=message.from_user.id, table_name='users')
    await pg_manager.close()
    if user_info:
        await message.answer(MESSAGES['hello'])
        await message.answer(MESSAGES['know_object'])
        await state.set_state(RegistrationStates.waiting_for_object)
    else:
        await message.answer(MESSAGES['know_name'])
        await state.set_state(RegistrationStates.waiting_for_name)


@user_router.message(RegistrationStates.waiting_for_name)
async def get_name_handler(message: Message, state: FSMContext):
    user_name = message.text
    await state.update_data(user_name=user_name)
    await message.answer(MESSAGES['know_role'],
                         reply_markup=role_kb(message.from_user.id))
    await state.set_state(RegistrationStates.waiting_for_role)


@user_router.message(RegistrationStates.waiting_for_role)
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

    try:
        await pg_manager.insert_data(
            table_name="users",
            records_data={
                "user_id": user_id,
                "full_name": user_name,
                "role": user_role
            }
        )
        await message.answer(f"Спасибо, {user_name}! Твоя роль '{user_role}' сохранена.")
        await message.answer(MESSAGES['know_object'], reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.waiting_for_object)
    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении данных: {e}")
        await state.clear()

    await pg_manager.close()


@user_router.message(RegistrationStates.waiting_for_object)
async def get_object_handler(message: Message, state: FSMContext):
    user_object = message.text
    await state.update_data(user_object=user_object)
    await message.answer(MESSAGES['know_system'])
    await state.set_state(RegistrationStates.waiting_for_system)


@user_router.message(RegistrationStates.waiting_for_system)
async def get_system_handler(message: Message, state: FSMContext):
    user_system = message.text
    await state.update_data(user_system=user_system)
    await message.answer(MESSAGES['know_spent_time'])
    await state.set_state(RegistrationStates.waiting_for_spent_time)


@user_router.message(RegistrationStates.waiting_for_spent_time)
async def get_spent_time_handler(message: Message, state: FSMContext):
    try:
        user_spent_time = int(message.text)
        if user_spent_time > 12 or user_spent_time < 1:
            await message.answer("Пожалуйста, введите корректное число часов. (Число от 1 до 12)")
            return
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число часов. (Число от 1 до 12)")
        return

    await state.update_data(user_spent_time=user_spent_time)
    await message.answer(MESSAGES['know_notes'])
    await state.set_state(RegistrationStates.waiting_for_notes)


@user_router.message(RegistrationStates.waiting_for_notes)
async def get_notes_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_notes = message.text
    user_data = await state.get_data()
    user_object = user_data.get('user_object')
    user_system = user_data.get('user_system')
    user_spent_time = user_data.get('user_spent_time')
    await state.update_data(user_name=user_notes)
    await pg_manager.connect()
    await pg_manager.create_table_records()

    try:
        await pg_manager.insert_data(
            table_name="records",
            records_data={
                "user_id": user_id,
                "object": user_object,
                "system": user_system,
                "spent_time": user_spent_time,
                "notes": user_notes
            }
        )
    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении данных: {e}")

    await state.clear()
    await pg_manager.close()
    await message.answer(MESSAGES['know_more'],
                         reply_markup=yes_no_kb(message.from_user.id))
    await state.set_state(RegistrationStates.waiting_for_more)


@user_router.message(RegistrationStates.waiting_for_more)
async def get_more_handler(message: Message, state: FSMContext):
    user_more = message.text
    await state.update_data(user_more=user_more)
    if user_more == 'Да':
        await pg_manager.connect()
        await message.answer(MESSAGES['know_object'], reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.waiting_for_object)
    else:
        await message.answer(MESSAGES['goodbye'], reply_markup=types.ReplyKeyboardRemove())
