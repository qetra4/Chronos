import asyncio
from create_bot import bot, dp
from scheduler import setup_scheduler, setup_scheduler_backup
from create_bot import pg_manager
from run import database_open
from handlers.handler_mounter import user_mounter_router
from handlers.handler_coder import user_coder_router
from handlers.handler_new_user import new_user_router
from handlers.handler_admin import admin_router
from handlers.handler_user_notification import notification_user_router
from handlers.handler_user_object import user_obj_router


async def main():
    dp.include_router(user_mounter_router)
    dp.include_router(user_coder_router)
    dp.include_router(new_user_router)
    dp.include_router(notification_user_router)
    dp.include_router(admin_router)
    dp.include_router(user_obj_router)
    await database_open(pg_manager)
    await pg_manager.setup_pool()
    await setup_scheduler(bot, pg_manager)
    await setup_scheduler_backup(bot, pg_manager)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await pg_manager.pool.close()

if __name__ == "__main__":
    asyncio.run(main())
