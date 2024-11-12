from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from create_bot import pg_manager
from handlers.states import RegistrationStates
from messages import MESSAGES
from keyboards import *
from decouple import config
from datetime import *

user_router = Router()


@user_router.message(F.text == "/start")
async def start_command_handler(message: Message, state: FSMContext):
    await pg_manager.connect()
    is_user_banned = await pg_manager.is_user_banned(user_id=message.from_user.id)
    if not is_user_banned:
        user_info = await pg_manager.get_user_data(user_id=message.from_user.id, table_name='users')
        await pg_manager.close()
        if user_info:
            await message.answer(MESSAGES['hello'])
            await message.answer(MESSAGES['know_object'], reply_markup=objects_kb(message.from_user.id))
            await state.set_state(RegistrationStates.waiting_for_object)
        else:
            await message.answer(MESSAGES['user_pass'])
            await state.set_state(RegistrationStates.waiting_for_password)


@user_router.message(RegistrationStates.waiting_for_password)
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
        await message.answer(MESSAGES['know_object'], reply_markup=objects_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_object)
    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении данных: {e}")
        await state.clear()

    await pg_manager.close()


@user_router.message(RegistrationStates.waiting_for_object)
async def get_object_handler(message: Message, state: FSMContext):
    user_object = message.text
    await state.update_data(user_object=user_object)
    await message.answer(MESSAGES['know_system'], reply_markup=systems_kb(message.from_user.id))
    await state.set_state(RegistrationStates.waiting_for_system)


@user_router.message(RegistrationStates.waiting_for_system)
async def get_system_handler(message: Message, state: FSMContext):
    user_system = message.text
    await state.update_data(user_system=user_system)
    if user_system == "АУД - Умный дом":
        await message.answer(MESSAGES['know_subsystem'], reply_markup=subsystems_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_subsystem)
    else:
        await message.answer(MESSAGES['know_type_of_work'], reply_markup=types_of_work_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_type_of_work)


@user_router.message(RegistrationStates.waiting_for_subsystem)
async def get_subsystem_handler(message: Message, state: FSMContext):
    user_subsystem = message.text
    await state.update_data(user_subsystem=user_subsystem)
    await message.answer(MESSAGES['know_type_of_work'], reply_markup=types_of_work_kb(message.from_user.id))
    await state.set_state(RegistrationStates.waiting_for_type_of_work)


@user_router.message(RegistrationStates.waiting_for_type_of_work)
async def get_type_of_work_handler(message: Message, state: FSMContext):
    user_type_of_work = message.text
    await state.update_data(user_type_of_work=user_type_of_work)
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
    today = datetime.now()
    user_id = message.from_user.id
    user_notes = message.text
    user_data = await state.get_data()
    user_object = user_data.get('user_object')
    user_system = user_data.get('user_system')
    user_subsystem = user_data.get('user_subsystem')
    user_type_of_work = user_data.get('user_type_of_work')
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
                "subsystem": user_subsystem,
                "work_type": user_type_of_work,
                "spent_time": user_spent_time,
                "date": today,
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
        await message.answer(MESSAGES['know_object'], reply_markup=objects_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_object)
    else:
        await message.answer(MESSAGES['goodbye'], reply_markup=types.ReplyKeyboardRemove())
