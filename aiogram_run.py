import asyncio
from create_bot import bot, dp
from scheduler import setup_scheduler
from create_bot import pg_manager
from handlers.handler_main_user import user_main_router
from handlers.handler_new_user import new_user_router
from handlers.handler_admin import admin_router
from handlers.handler_user_notification import notification_user_router


async def main():
    dp.include_router(user_main_router)
    dp.include_router(new_user_router)
    dp.include_router(notification_user_router)
    dp.include_router(admin_router)
    await pg_manager.setup_pool()
    await setup_scheduler(bot, pg_manager)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await pg_manager.pool.close()

if __name__ == "__main__":
    asyncio.run(main())
