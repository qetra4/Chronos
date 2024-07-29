import asyncio
from aiogram import Bot, Dispatcher
from handlers import user_private_router
import logging
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(user_private_router)
logging.basicConfig(level=logging.INFO)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
