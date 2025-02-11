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
        keyboard = await user_objects_kb(message.from_user.id)
        await message.answer(MESSAGES['user_obj_show'], reply_markup=keyboard)
        await state.set_state(RegistrationStates.waiting_for_tap_to_hide_keyboard)
    elif user_obj_what == 'Добавить кнопку':
        await pg_manager.connect()
        count_objects = await pg_manager.count_records(table_name='objects')
        count_user_objects = await pg_manager.count_records_for_certain_user(user_id=message.from_user.id,
                                                                             table_name="user_keyboard")
        print(count_user_objects, count_objects)
        if count_user_objects == count_objects:
            await message.answer(MESSAGES['user_obj_add_false'], reply_markup=types.ReplyKeyboardRemove())
        else:
            keyboard = await left_objects_kb(message.from_user.id)
            await message.answer(MESSAGES['user_obj_add_true'], reply_markup=keyboard)
            await state.set_state(RegistrationStates.waiting_for_tap_to_add_button)
    elif user_obj_what == 'Удалить кнопку':
        await pg_manager.connect()
        count_objects = await pg_manager.count_records(table_name='objects')
        await pg_manager.close()
        if count_objects < 2:
            await message.answer(MESSAGES['user_obj_delete_false'], reply_markup=types.ReplyKeyboardRemove())
        else:
            keyboard = await user_objects_kb(message.from_user.id)
            await message.answer(MESSAGES['user_obj_delete_true'], reply_markup=keyboard)
            await state.set_state(RegistrationStates.waiting_for_tap_to_delete_button)


@user_obj_router.message(RegistrationStates.waiting_for_tap_to_hide_keyboard)
async def show_keyboard_handler(message: Message, state: FSMContext):
    await message.answer("Клавиатура закрыта :)", reply_markup=types.ReplyKeyboardRemove())


@user_obj_router.message(RegistrationStates.waiting_for_tap_to_add_button)
async def add_button_handler(message: Message, state: FSMContext):
    object_name = message.text
    user_id = message.from_user.id
    await state.update_data(object_name=object_name)
    await pg_manager.connect()
    try:
        await pg_manager.insert_data(
            table_name="user_keyboard",
            records_data={
                "user_id": user_id,
                "object_name": object_name
            }
        )
    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении данных: {e}")
    await pg_manager.close()
    await message.answer("Успех!")


@user_obj_router.message(RegistrationStates.waiting_for_tap_to_delete_button)
async def delete_button_handler(message: Message, state: FSMContext):
    object_name = message.text
    user_id = message.from_user.id
    await state.update_data(object_name=object_name)
    await pg_manager.connect()
    await pg_manager.delete_data(table_name='user_keyboard',
                                 where_dict={"user_id": user_id, 'object_name': object_name})
    await pg_manager.close()
    await message.answer("Успех!")
