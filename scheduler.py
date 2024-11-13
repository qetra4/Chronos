from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from handlers.db_handler import PostgresHandler
from aiogram import Bot
from datetime import datetime


async def send_daily_notifications(bot: Bot, pg_manager: PostgresHandler):
    await pg_manager.connect()
    today_date = datetime.now()
    try:
        user_ids = await pg_manager.get_all_user_ids()
        for user_id in user_ids:
            is_record_user_today = await pg_manager.is_user_record_today(user_id, today_date)
            print(is_record_user_today)
            if not is_record_user_today:
                await bot.send_message(user_id,
                                       "Напоминание: не забудь рассказать о своих сегодняшних свершениях :)")
    finally:
        await pg_manager.close()


def setup_scheduler(bot: Bot, pg_manager: PostgresHandler):
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        send_daily_notifications,
        CronTrigger(day_of_week="mon-fri", hour=12, minute=5),
        args=[bot, pg_manager]
    )

    scheduler.add_job(
        send_daily_notifications,
        CronTrigger(day_of_week="mon-fri", hour=12, minute=7),
        args=[bot, pg_manager]
    )

    scheduler.start()
