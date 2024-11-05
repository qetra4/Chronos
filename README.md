# Chronos
Tg-bot written with aiogram3. Used to collect statistics data about implementation activity.\
It supports authorization, notifications, admin menu and data exchange with AirTable.

## Requirements
To start the project you will need the following:

- **Python+**
- **pip**
- **virtualenv**

### Python Dependencies:
- **asyncpg**
- **aiogram**
- **APScheduler**
- **python-decouple**
- 
## Installation
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
