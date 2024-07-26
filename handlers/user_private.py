from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram import F


user_private_router = Router()


@user_private_router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Конечно! Да здравствует Макаронный Монстр!")],
        [types.KeyboardButton(text="Спасибо, я, пожалуй, пойду")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Соглашайтесь"

    )
    await message.answer("Доброго времени суток! Я - бот, призванный собирать пожертвования во славу "
                                 "Летающего Макаронного Монстра. Хотите сделать пожертвование?", reply_markup=keyboard)


@user_private_router.message(F.text.lower() == "конечно! да здравствует макаронный монстр!")
async def with_puree(message: types.Message):
    await message.reply("Превосходно! Займемся делом!", reply_markup=types.ReplyKeyboardRemove())


@user_private_router.message(F.text.lower() == "спасибо, я, пожалуй, пойду")
async def without_puree(message: types.Message):
    await message.reply("Мы всегда будем ждать вас назад, ведь все дороги ведут к просветлению")
