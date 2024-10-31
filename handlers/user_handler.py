# handlers/user_handler.py
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
    await message.answer(MESSAGES['know_name'])
    # Устанавливаем состояние ожидания имени
    await state.set_state(RegistrationStates.waiting_for_name)


# Обработчик для получения имени пользователя
@user_router.message(RegistrationStates.waiting_for_name)
async def get_name_handler(message: Message, state: FSMContext):
    user_name = message.text
    user_id = message.from_user.id
    await state.update_data(user_name=user_name)
    await state.set_state(RegistrationStates.waiting_for_role)
    await message.answer(MESSAGES['know_role'],
                         reply_markup=role_kb(message.from_user.id))


# Обработчик для получения роли пользователя и сохранения в базе данных
@user_router.message(RegistrationStates.waiting_for_role)
async def get_role_handler(message: Message, state: FSMContext):
    user_role = message.text
    user_data = await state.get_data()

    # Получаем имя пользователя из состояния
    user_name = user_data.get('user_name')
    user_id = message.from_user.id

    # Проверка на наличие имени
    if user_name is None:
        await message.answer("Произошла ошибка: не удалось получить имя пользователя.")
        await state.clear()
        return

    # Проверка на наличие user_id
    if user_id is None:
        await message.answer("Произошла ошибка: не удалось получить идентификатор пользователя.")
        await state.clear()
        return

    await pg_manager.connect()
    await pg_manager.create_table()

    # Сохраняем данные в базе
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

    # Завершаем состояние
    await state.clear()
    await pg_manager.close()
