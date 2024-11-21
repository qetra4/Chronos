from aiogram import Router, F
from aiogram.types import Message
from handlers.states import RegistrationStates
from messages import MESSAGES
from keyboards import *
from aiogram import types
from aiogram.fsm.context import FSMContext

user_obj_router = Router()


@user_obj_router.message(F.text == "/set_objects")
async def set_objects_handler(message: Message, state: FSMContext):
    await pg_manager.connect()
    is_user_banned = await pg_manager.is_user_banned(user_id=message.from_user.id)
    if not is_user_banned:
        user_info = await pg_manager.get_user_data(user_id=message.from_user.id, table_name='users')
        if user_info:
            await message.answer(MESSAGES['user_obj_what_to_do'], reply_markup=user_obj_what_to_do(message.from_user.id))
            await state.set_state(RegistrationStates.waiting_for_obj_what_to_do)
        else:
            await message.answer(MESSAGES['user_pass'], reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(RegistrationStates.waiting_for_password)
    await pg_manager.close()


@user_obj_router.message(RegistrationStates.waiting_for_obj_what_to_do)
async def get_obj_what_to_do(message: types.Message, state: FSMContext):
    user_obj_what = message.text
    if user_obj_what == 'Отобразить текущую клавиатуру':
        keyboard = await objects_kb(message.from_user.id)
        await message.answer(MESSAGES['user_obj_show'], reply_markup=keyboard)
        await state.set_state(RegistrationStates.waiting_for_tap_to_hide_keyboard)
    elif user_obj_what == 'Добавить кнопку':
        await message.answer(MESSAGES['user_obj_what_to_do'], reply_markup=user_obj_what_to_do(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_tap_to_add_button)
    elif user_obj_what == 'Удалить кнопку':
        keyboard = await objects_kb(message.from_user.id)
        await message.answer(MESSAGES['user_obj_what_to_do'], reply_markup=keyboard)
        await state.set_state(RegistrationStates.waiting_for_tap_to_delete_button)


@user_obj_router.message(RegistrationStates.waiting_for_tap_to_hide_keyboard)
async def show_keyboard_handler(message: Message, state: FSMContext):
    await message.answer("Клавиатура закрыта :)", reply_markup=types.ReplyKeyboardRemove())


@user_obj_router.message(RegistrationStates.waiting_for_tap_to_add_button)
async def add_button_handler(message: Message, state: FSMContext):
    user_subsystem = message.text
    await state.update_data(user_subsystem=user_subsystem)
    keyboard = await types_of_work_kb(message.from_user.id)
    await message.answer(MESSAGES['know_type_of_work'], reply_markup=keyboard)
    await state.set_state(RegistrationStates.waiting_for_type_of_work)


@user_obj_router.message(RegistrationStates.waiting_for_subsystem)
async def delete_button_handler(message: Message, state: FSMContext):
    user_subsystem = message.text
    await state.update_data(user_subsystem=user_subsystem)
    keyboard = await types_of_work_kb(message.from_user.id)
    await message.answer(MESSAGES['know_type_of_work'], reply_markup=keyboard)
    await state.set_state(RegistrationStates.waiting_for_type_of_work)

