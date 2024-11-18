from aiogram import Router, F
from aiogram.types import Message
from create_bot import pg_manager, bot
from handlers.states import RegistrationStates
from messages import MESSAGES
from aiogram import types
from aiogram.fsm.context import FSMContext
from scheduler import schedule_user_notifications

notification_user_router = Router()


@notification_user_router.message(F.text == "/set_notifications")
async def set_notifications_command_handler(message: Message, state: FSMContext):
    await pg_manager.connect()
    is_user_banned = await pg_manager.is_user_banned(user_id=message.from_user.id)
    if not is_user_banned:
        user_info = await pg_manager.get_user_data(user_id=message.from_user.id, table_name='users')
        if user_info:
            await message.answer(MESSAGES['notifications_time'], reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(RegistrationStates.waiting_for_hour)
        else:
            await message.answer(MESSAGES['user_pass'], reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(RegistrationStates.waiting_for_password)
    await pg_manager.close()


@notification_user_router.message(RegistrationStates.waiting_for_hour)
async def get_hour(message: types.Message, state: FSMContext):
    try:
        user_hour = int(message.text)
        if 0 <= user_hour <= 23:
            await state.update_data(user_hour=user_hour)
            await message.answer(MESSAGES['got_hours'])
            await state.set_state(RegistrationStates.waiting_for_minute)
        else:
            await message.answer(MESSAGES['diaposon_error_hours'])
    except ValueError:
        await message.answer(MESSAGES['value_error'])


@notification_user_router.message(RegistrationStates.waiting_for_minute)
async def get_minute(message: types.Message, state: FSMContext):
    try:
        minutes = int(message.text)
        if 0 <= minutes <= 59:
            user_data = await state.get_data()
            hour = user_data.get('user_hour')
            user_id = message.from_user.id
            await pg_manager.connect()
            await pg_manager.create_notifications_table()
            try:
                await pg_manager.delete_data(
                    table_name="notifications",
                    where_dict={"user_id": user_id}
                )
            except Exception as e:
                print(f"Error while deleting user notifications for user_id={user_id}:", e)
            try:
                await pg_manager.insert_data(
                    table_name="notifications",
                    records_data={
                        "user_id": user_id,
                        "hour": hour,
                        "minutes": minutes
                    }
                )
            except Exception as e:
                await message.answer(f"Произошла ошибка при сохранении данных: {e}")
            await message.answer(f"Уведомления будут отправляться в {hour:02d}:{minutes:02d} с понедельника по пятницу.")
            await state.clear()
            await schedule_user_notifications(bot, pg_manager)
        else:
            await message.answer(MESSAGES['diaposon_error_minutes'])
    except ValueError:
        await message.answer(MESSAGES['value_error'])
    finally:
        await pg_manager.close()

