from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from create_bot import pg_manager  # Экземпляр PostgresHandler
from handlers.states import RegistrationStates
from messages import MESSAGES
from keyboards import role_kb

user_router = Router()


@user_router.message(F.text == "/start")
async def start_command_handler(message: Message, state: FSMContext):
    await pg_manager.connect()
    user_info = await pg_manager.get_user_data(user_id=message.from_user.id, table_name='users')
    if user_info:
        response_text = f'{user_info.get("full_name")}, Вижу что вы уже в моей базе данных'
        await message.answer('вай вай вай привет брат')
    else:
        await message.answer(MESSAGES['know_name'])
        await state.set_state(RegistrationStates.waiting_for_name)


@user_router.message(RegistrationStates.waiting_for_name)
async def get_name_handler(message: Message, state: FSMContext):
    user_name = message.text
    user_id = message.from_user.id
    await state.update_data(user_name=user_name)
    await state.set_state(RegistrationStates.waiting_for_role)
    await message.answer(MESSAGES['know_role'],
                         reply_markup=role_kb(message.from_user.id))


@user_router.message(RegistrationStates.waiting_for_role)
async def get_role_handler(message: Message, state: FSMContext):
    user_role = message.text
    user_data = await state.get_data()
    user_name = user_data.get('user_name')
    user_id = message.from_user.id

    if user_name is None:
        await message.answer("Произошла ошибка: не удалось получить имя пользователя.")
        await state.clear()
        return

    if user_id is None:
        await message.answer("Произошла ошибка: не удалось получить идентификатор пользователя.")
        await state.clear()
        return

    await pg_manager.create_table()

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
    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении данных: {e}")

    await state.clear()
    await pg_manager.close()
