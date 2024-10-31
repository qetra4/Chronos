# Chronos
Tg-bot written with aiogram3. Used to collect statistics data about implementation activity.\
It supports authorization, notifications, admin menu and data exchange with AirTable.

## Требования
Для запуска проекта вам понадобится следующее:

- **Python 3.8 или выше** — для выполнения основного кода
- **pip** — для установки зависимостей
- **virtualenv** — для создания виртуального окружения

### Зависимости Python:
- **asyncpg** — библиотека для асинхронной работы с PostgreSQL
- **aiogram** — фреймворк для создания Telegram-ботов
- **APScheduler** — для планирования задач
- **python-decouple** — для управления конфигурацией с использованием переменных окружения

## Установка
1. Clone the repository
2. Create a virtual environment
3. Install dependencies
```sh
pip install -r requirements.txt
```
4. Create an .env file in the root of the project and add the following variables to it:
```
TOKEN=your_bot_token
ADMINS=admin1_tg_id, admin2_tg_id
ROOT_PASS=234234g531KKK33
PG_LINK=postgresql://username:password@host:port/dbname
```
Substitute your own data. By the way, you need to find out your telegram ID, create a bot token and deploy a database.

5. Run the bot and enjoy the result
```sh
python aiogram_run.py
```
