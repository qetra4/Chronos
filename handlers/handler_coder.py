from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import RegistrationStates
from messages import MESSAGES
from keyboards import *
from datetime import datetime, timedelta
from functions import func_main

user_coder_router = Router()


@user_coder_router.message(RegistrationStates.waiting_for_info_coder)
async def get_info_handler(message: Message, state: FSMContext):
    user_info = message.text
    await state.update_data(user_info=user_info)
    if user_info == 'Да, расскажу':
        keyboard = await user_objects_kb(message.from_user.id)
        await message.answer(MESSAGES['know_object'], reply_markup=keyboard)
        today = datetime.now().date()
        await state.update_data(user_today=today)
        await state.set_state(RegistrationStates.waiting_for_object_coder)
    else:
        today = datetime.now().date()
        await state.update_data(user_today=today)        
        await message.answer(MESSAGES['why_not'], reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.waiting_for_notes_coder)



