from handlers.handler_db import PostgresHandler
from create_bot import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from aiogram import Bot
import subprocess, os
from decouple import config


async def send_notification(chat_id):
    """Send a scheduled notification to the user."""
    await bot.send_message(chat_id, "Напоминание: не забудь рассказать о своих сегодняшних свершениях :)")


async def schedule_user_notifications(bot: Bot, pg_manager: PostgresHandler):
    """Schedule user-specific notifications."""
    scheduler = AsyncIOScheduler(timezone="UTC")
    async with pg_manager.pool.acquire() as connection:
        today_date = datetime.now().date()
        user_data = await connection.fetch("SELECT user_id, hour, minutes FROM notifications")
        for record in user_data:
            is_record_user_today = await pg_manager.is_user_record_today(record["user_id"], today_date)
            if not is_record_user_today:
                scheduler.add_job(
                    send_notification,
                    CronTrigger(day_of_week="mon-fri", hour=record["hour"], minute=record["minutes"]),
                    args=[record["user_id"]]
                )
    scheduler.start()


async def send_daily_notifications(bot: Bot, pg_manager: PostgresHandler):
    """Send daily reminder notifications."""
    await pg_manager.setup_pool()
    async with pg_manager.pool.acquire() as connection:
        today_date = datetime.now().date()
        try:
            user_ids = await pg_manager.get_all_user_ids()
            users_with_custom_notifications = await pg_manager.get_users_with_custom_notifications()
            for user_id in user_ids:
                if user_id not in users_with_custom_notifications:
                    is_record_user_today = await pg_manager.is_user_record_today(user_id, today_date)
                    if not is_record_user_today:
                        await bot.send_message(
                            user_id,
                            "Напоминание: не забудь рассказать о своих сегодняшних свершениях :)"
                        )
        except Exception as e:
            print("Error while sending daily notifications:", e)


async def setup_scheduler(bot: Bot, pg_manager: PostgresHandler):

    scheduler = AsyncIOScheduler(timezone="UTC")
    await schedule_user_notifications(bot, pg_manager)

    scheduler.add_job(
        send_daily_notifications,
        CronTrigger(day_of_week="mon-fri", hour=16, minute=50),
        args=[bot, pg_manager]
    )

    scheduler.add_job(
        send_daily_notifications,
        CronTrigger(day_of_week="mon-fri", hour=16, minute=25),
        args=[bot, pg_manager]
    )

    scheduler.add_job(
        send_daily_notifications,
        CronTrigger(day_of_week="mon-fri", hour=17, minute=50),
        args=[bot, pg_manager]
    )

    scheduler.start()

async def backup_database():
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    directory = config('DIRECTORY')
    backup_file = os.path.join(directory, f"backup_{now}.sql")
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.environ['PGPASSWORD'] = '12345'
    command = [
        "pg_dump",
        "--host=localhost",
        "--port=5432",
        "--username=postgres",
        "--file", backup_file,
        "--format=plain", 
        "postgres"
    ]
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Бэкап успешно создан: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании бэкапа: {e.stderr}")


async def setup_scheduler_backup(bot: Bot, pg_manager: PostgresHandler):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(backup_database, "cron", hour=9, minute=6)
    scheduler.start()
