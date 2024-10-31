from aiogram import types, F, Router
from aiogram.filters import Command
from messages import MESSAGES
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType
from config import *
"""
user_private_router = Router()

PRICES = [
    LabeledPrice(label='Щедрое пожертвование', amount=5000)
]


@user_private_router.message(Command("start"))
async def start_cmd(message: Message):

    await message.answer(MESSAGES['start'])

@user_private_router.message(Command("."))
async def start_cmd(message: Message):
    roles = [
        [types.KeyboardButton(text="Монтажник")],
        [types.KeyboardButton(text="Программист")],
        [types.KeyboardButton(text="Руководитель проекта")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=roles,
        resize_keyboard=True,
        input_field_placeholder="Соглашайтесь")

    await message.answer(MESSAGES['start'], reply_markup=keyboard)

@user_private_router.message(F.text.lower() == "конечно! да здравствует макаронный монстр!")
async def buy(message: types.Message):
    await message.reply("Превосходно! Займемся делом!", reply_markup=types.ReplyKeyboardRemove())
    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title=MESSAGES['item_title'],
        description=MESSAGES['item_description'],
        payload='some_invoice',
        provider_token=PAYMENTS_TOKEN,
        currency='rub',
        prices=PRICES,
        start_parameter='example',
        photo_url=item_url,
        photo_height=250,
        photo_width=250,
        photo_size=250,
        need_email=True,
        need_phone_number=False,
        need_shipping_address=False,
        is_flexible=False
    )


@user_private_router.pre_checkout_query(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@user_private_router.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await message.answer(
        MESSAGES['successful_payment'].format(
            total_amount=message.successful_payment.total_amount // 100,
            currency=message.successful_payment.currency
        )
    )


@user_private_router.message(F.text.lower() == "Монтажник")
async def be_back(message: types.Message):
    await message.reply("Превосходно! Теперь мы можем работать вместе.")


@user_private_router.message(F.text.lower() == "Программист")
async def be_back(message: types.Message):
    await message.reply("Превосходно! Теперь мы можем работать вместе.")


@user_private_router.message(F.text.lower() == "Руководитель проекта")
async def be_back(message: types.Message):
    await message.reply("Превосходно! Теперь мы можем работать вместе.")
"""
