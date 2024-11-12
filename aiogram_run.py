import asyncio
from create_bot import bot, dp
from handlers.user_main_handler import user_main_router
from handlers.new_user_hadler import new_user_router
from handlers.admin_handler import admin_router


async def main():
    dp.include_router(user_main_router)
    dp.include_router(new_user_router)
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
