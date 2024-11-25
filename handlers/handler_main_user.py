from aiogram import Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import RegistrationStates
from messages import MESSAGES
from keyboards import *
from datetime import datetime

user_main_router = Router()


@user_main_router.message(RegistrationStates.waiting_for_info)
async def get_info_handler(message: Message, state: FSMContext):
    user_info = message.text
    await state.update_data(user_info=user_info)
    if user_info == 'Да, расскажу':
        keyboard = await objects_kb(message.from_user.id)
        await message.answer(MESSAGES['know_object'], reply_markup=keyboard)
        await state.set_state(RegistrationStates.waiting_for_object)
    else:
        await message.answer(MESSAGES['why_not'], reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.waiting_for_notes)


@user_main_router.message(RegistrationStates.waiting_for_object)
async def get_object_handler(message: Message, state: FSMContext):
    user_object = message.text
    await state.update_data(user_object=user_object)
    keyboard = await systems_kb(message.from_user.id)
    await message.answer(MESSAGES['know_system'], reply_markup=keyboard)
    await state.set_state(RegistrationStates.waiting_for_system)


@user_main_router.message(RegistrationStates.waiting_for_system)
async def get_system_handler(message: Message, state: FSMContext):
    user_system = message.text
    await state.update_data(user_system=user_system)
    if user_system == "АУД - Умный дом":
        keyboard = await subsystems_kb(message.from_user.id)
        await message.answer(MESSAGES['know_subsystem'], reply_markup=keyboard)
        await state.set_state(RegistrationStates.waiting_for_subsystem)
    else:
        keyboard = await types_of_work_kb(message.from_user.id)
        await message.answer(MESSAGES['know_type_of_work'], reply_markup=keyboard)
        await state.set_state(RegistrationStates.waiting_for_type_of_work)


@user_main_router.message(RegistrationStates.waiting_for_subsystem)
async def get_subsystem_handler(message: Message, state: FSMContext):
    user_subsystem = message.text
    await state.update_data(user_subsystem=user_subsystem)
    keyboard = await types_of_work_kb(message.from_user.id)
    await message.answer(MESSAGES['know_type_of_work'], reply_markup=keyboard)
    await state.set_state(RegistrationStates.waiting_for_type_of_work)


@user_main_router.message(RegistrationStates.waiting_for_type_of_work)
async def get_type_of_work_handler(message: Message, state: FSMContext):
    user_type_of_work = message.text
    await state.update_data(user_type_of_work=user_type_of_work)
    await message.answer(MESSAGES['know_extra'], reply_markup=yes_no_kb(message.from_user.id))
    await state.set_state(RegistrationStates.waiting_for_extra)


@user_main_router.message(RegistrationStates.waiting_for_extra)
async def get_extra_handler(message: Message, state: FSMContext):
    user_extra = message.text
    await state.update_data(user_extra=user_extra)
    await message.answer(MESSAGES['know_spent_time'])
    await state.set_state(RegistrationStates.waiting_for_spent_time)


@user_main_router.message(RegistrationStates.waiting_for_spent_time)
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


@user_main_router.message(RegistrationStates.waiting_for_notes)
async def get_notes_handler(message: Message, state: FSMContext):
    today = datetime.now()
    user_id = message.from_user.id
    user_notes = message.text
    user_data = await state.get_data()
    user_object = user_data.get('user_object')
    user_system = user_data.get('user_system')
    user_subsystem = user_data.get('user_subsystem')
    user_type_of_work = user_data.get('user_type_of_work')
    user_extra = user_data.get('user_extra')
    user_spent_time = user_data.get('user_spent_time')
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
                "extra": user_extra,
                "date": today,
                "notes": user_notes
            }
        )
    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении данных: {e}")
    if user_object is not None:
        await message.answer(MESSAGES['know_more'],
                             reply_markup=yes_no_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_more)
    else:
        await state.clear()
        await message.answer(MESSAGES['goodbye'])


@user_main_router.message(RegistrationStates.waiting_for_more)
async def get_more_handler(message: Message, state: FSMContext):
    user_more = message.text
    await state.update_data(user_more=user_more)
    if user_more == 'Да':
        await state.update_data(user_subsystem=None)
        await pg_manager.connect()
        await message.answer(MESSAGES['same_object'], reply_markup=yes_no_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_same_object)
    else:
        await message.answer(MESSAGES['goodbye'], reply_markup=types.ReplyKeyboardRemove())
        await state.clear()


@user_main_router.message(RegistrationStates.waiting_for_same_object)
async def waiting_for_same_object(message: Message, state: FSMContext):
    user_same = message.text
    if user_same == 'Да':
        keyboard = await systems_kb(message.from_user.id)
        await message.answer(MESSAGES['know_system'], reply_markup=keyboard)
        await state.set_state(RegistrationStates.waiting_for_system)
    else:
        keyboard = await objects_kb(message.from_user.id)
        await message.answer(MESSAGES['know_object'], reply_markup=keyboard)
        await state.set_state(RegistrationStates.waiting_for_object)
