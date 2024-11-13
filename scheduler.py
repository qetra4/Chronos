from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from handlers.db_handler import PostgresHandler
from aiogram import Bot


async def send_daily_notifications(bot: Bot, db_manager: PostgresHandler):
    await db_manager.connect()
    try:
        user_ids = await db_manager.get_all_user_ids()
        for user_id in user_ids:
            await bot.send_message(user_id, "Напоминание: не забудь рассказать о своих сегодняшних свершениях :)")
    finally:
        await db_manager.close()


def setup_scheduler(bot: Bot, db_manager: PostgresHandler):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_daily_notifications,
        CronTrigger(day_of_week="mon-fri", hour=19, minute=00),
        args=[bot, db_manager]
    )
    scheduler.start()

