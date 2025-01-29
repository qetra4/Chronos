from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import RegistrationStates
from messages import MESSAGES
from keyboards import *
from datetime import datetime, timedelta
from functions import func_main

user_main_router = Router()

@user_main_router.message(F.text == "/choose_date_to_answer")
async def start_command_handler(message: Message, state: FSMContext):
    await pg_manager.connect()
    is_user_banned = await pg_manager.is_user_banned(user_id=message.from_user.id)
    if not is_user_banned:
        user_info = await pg_manager.get_user_data(user_id=message.from_user.id, table_name='users')
        if user_info:
            await message.answer(MESSAGES['know_period'], reply_markup=period_kb(message.from_user.id))
            await state.set_state(RegistrationStates.waiting_for_period)
        else:
            await message.answer(MESSAGES['user_pass'])
            await state.set_state(RegistrationStates.waiting_for_password)
    await pg_manager.close()


@user_main_router.message(RegistrationStates.waiting_for_period)
async def get_info_handler(message: Message, state: FSMContext):
    user_info = message.text
    if user_info == 'Вчера':
        date_fill = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
        date_fill = datetime.strptime(date_fill, '%Y-%m-%d')
        await state.update_data(user_date=date_fill)
        await message.answer(MESSAGES['intention_not_today'], reply_markup=tell_info_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_info)
    elif user_info == 'Завтра':
        date_fill = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
        date_fill = datetime.strptime(date_fill, '%Y-%m-%d')
        await state.update_data(user_date=date_fill)
        await message.answer(MESSAGES['intention_not_today'], reply_markup=tell_info_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_info)
    elif user_info == 'За выбранную мной дату':
        await message.answer(MESSAGES['choose_date'])
        await state.set_state(RegistrationStates.waiting_for_date)
    elif user_info == 'По выбранный мной день включительно':    
        await message.answer(MESSAGES['choose_date_period'])
        await state.set_state(RegistrationStates.waiting_for_date_period)


@user_main_router.message(RegistrationStates.waiting_for_date)
async def get_info_handler(message: types.Message, state: FSMContext):
    date_fill = message.text
    try:
        date_fill = datetime.strptime(date_fill, '%d-%m-%Y').date()
        await state.update_data(user_date=date_fill)
        await message.answer(MESSAGES['intention_not_today'], reply_markup=tell_info_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_info)
    except ValueError:
        await message.answer("Некорректный формат даты. Пожалуйста, используйте ДД-ММ-ГГГГ.")


@user_main_router.message(RegistrationStates.waiting_for_date_period)
async def get_date_period_handler(message: Message, state: FSMContext):
    date_fill = message.text
    try:
        date_fill = datetime.strptime(date_fill, '%d-%m-%Y').date()
        await state.update_data(user_till_date=date_fill)
        print("date_fill", date_fill)
        await message.answer(MESSAGES['intention_not_today'], reply_markup=tell_info_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_info)
    except ValueError:
        await message.answer("Некорректный формат даты. Пожалуйста, используйте ДД-ММ-ГГГГ.")


@user_main_router.message(RegistrationStates.waiting_for_info)
async def get_info_handler(message: Message, state: FSMContext):
    user_info = message.text
    await state.update_data(user_info=user_info)
    if user_info == 'Да, расскажу':
        keyboard = await user_objects_kb(message.from_user.id)
        await message.answer(MESSAGES['know_object'], reply_markup=keyboard)
        today = datetime.now().date()
        await state.update_data(user_today=today)
        await state.set_state(RegistrationStates.waiting_for_object)
    else:
        today = datetime.now().date()
        await state.update_data(user_today=today)        
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
    await message.answer(MESSAGES['know_notes'],  reply_markup=yes_no_kb(message.from_user.id))
    await state.set_state(RegistrationStates.waiting_for_if_notes)    


@user_main_router.message(RegistrationStates.waiting_for_if_notes)
async def get_if_notes(message: Message, state: FSMContext):
    user_if_notes = message.text

    if user_if_notes == 'Да':
        await message.answer(MESSAGES['what_notes'])
        await state.set_state(RegistrationStates.waiting_for_notes)
    else:
        user_id = message.from_user.id
        user_data = await state.get_data()
        user_date = user_data.get('user_date')
        today = user_data.get('user_today')
        user_object = user_data.get('user_object')
        user_notes = "-"
        await state.update_data(user_notes=user_notes)
        await func_main.write_notes_handler(user_id, state)
        await state.update_data(user_notes=user_notes)    
        if (user_object is not None) and (user_date == today):
            await message.answer(MESSAGES['know_more'],
                                reply_markup=yes_no_kb(message.from_user.id))
            await state.set_state(RegistrationStates.waiting_for_more)
        else:
            await state.clear()
            await message.answer(MESSAGES['goodbye'], reply_markup=types.ReplyKeyboardRemove())


@user_main_router.message(RegistrationStates.waiting_for_notes)
async def get_notes_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await state.get_data()
    user_date = user_data.get('user_date')
    today = user_data.get('user_today')
    user_object = user_data.get('user_object')
    user_system = user_data.get('user_system')
    user_type_of_work = user_data.get('user_type_of_work')
    user_notes = message.text
    await state.update_data(user_notes=user_notes)
    if user_object == 'Прочее' and user_system == 'Прочее' and user_type_of_work == 'Прочее' and user_notes == '-':
        await message.answer("Вы не ввели никакой уточнящей информации к проделанной работе, так что комментарий обязателен.")
        return
    await func_main.write_notes_handler(user_id, state)
    if (user_object is not None) and (user_date == today):
        await message.answer(MESSAGES['know_more'],
                             reply_markup=yes_no_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_more)
    else:
        await state.clear()
        await message.answer(MESSAGES['goodbye'], reply_markup=types.ReplyKeyboardRemove())


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
        keyboard = await user_objects_kb(message.from_user.id)
        await message.answer(MESSAGES['know_object'], reply_markup=keyboard)
        await state.set_state(RegistrationStates.waiting_for_object)
