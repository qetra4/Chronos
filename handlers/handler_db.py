import asyncpg
from typing import Dict, Any, Optional, List


class PostgresHandler:
    def __init__(self, dsn: str):
        print("Initializing connection to the database with DSN:", dsn)
        self.dsn = dsn
        self.connection = None
        self.pool = None

    async def setup_pool(self):
        """Setup connection pool."""
        self.pool = await asyncpg.create_pool(self.dsn)

    async def get_all_user_ids(self):
        async with self.pool.acquire() as connection:
            records = await connection.fetch("SELECT user_id FROM users")
            return [record['user_id'] for record in records]

    async def get_users_with_custom_notifications(self):
        async with self.pool.acquire() as connection:
            records = await connection.fetch("SELECT user_id FROM notifications")
            return [record['user_id'] for record in records]

    async def get_notifications_data(self, table_name='notifications'):
        async with self.pool.acquire() as connection:
            query = f"SELECT user_id, hour, minutes FROM {table_name} WHERE hour IS NOT NULL AND minutes IS NOT NULL"
            rows = await connection.fetch(query)
            user_data = {row['user_id']: {'hour': row['hour'], 'minutes': row['minutes']} for row in rows}
            return user_data

    async def is_user_record_today(self, user_id, date):
        async with self.pool.acquire() as connection:
            result = await connection.fetchval(
                "SELECT EXISTS(SELECT 1 FROM records WHERE user_id = $1 AND date = $2)",
                user_id, date
            )
            return result

    async def connect(self):
        self.connection = await asyncpg.connect(self.dsn)

    async def close(self):
        await self.connection.close()

    async def create_table_users(self):
        try:
            await self.connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    full_name VARCHAR(50),
                    role TEXT
                );
            """)
            print("Table users created or already exists.")
        except Exception as e:
            print("Error while creating table users:", e)

    async def create_table_records(self):
        try:
            await self.connection.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    record_id SERIAL PRIMARY KEY,
                    user_id BIGINT REFERENCES users(user_id),
                    object TEXT,
                    system TEXT,
                    subsystem TEXT,
                    work_type TEXT,
                    extra TEXT,
                    spent_time INT,
                    date DATE,
                    notes VARCHAR(255)
                );
            """)
            print("Table records created or already exists.")
        except Exception as e:
            print("Error while creating table records:", e)

    async def create_notifications_table(self):
        try:
            await self.connection.execute("""
             CREATE TABLE IF NOT EXISTS notifications (
                not_data_id SERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
                hour INT,
                minutes INT
             );
             """)
            print("Table ban created or already exists.")
        except Exception as e:
            print("Error while creating table ban:", e)

    async def has_user_set_notifications(self, user_id, today):
        return await self.connection.fetchval("SELECT hour FROM notifications WHERE user_id = $1",
                                              user_id) is not None

    async def create_user_keyboard_table(self):
        try:
            await self.connection.execute("""
             CREATE TABLE IF NOT EXISTS user_keyboard (
                button_id SERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
                object_name VARCHAR
             );
             """)
            print("Table user_keyboard created or already exists.")
        except Exception as e:
            print("Error while creating table ban:", e)

    async def create_ban_table(self):
        try:
            await self.connection.execute("""
             CREATE TABLE IF NOT EXISTS banned_users (
             user_id BIGINT PRIMARY KEY
             );
             """)
            print("Table ban created or already exists.")
        except Exception as e:
            print("Error while creating table ban:", e)

    async def create_objects_table(self):
        try:
            await self.connection.execute("""
             CREATE TABLE IF NOT EXISTS objects (
             object_id SERIAL PRIMARY KEY,
             object_name VARCHAR
             );
             """)
            print("Table ban created or already exists.")
        except Exception as e:
            print("Error while creating table ban:", e)

    async def create_systems_table(self):
        try:
            await self.connection.execute("""
             CREATE TABLE IF NOT EXISTS systems (
             system_id SERIAL PRIMARY KEY,
             system_name VARCHAR
             );
             """)
            print("Table ban created or already exists.")
        except Exception as e:
            print("Error while creating table ban:", e)

    async def create_subsystems_table(self):
        try:
            await self.connection.execute("""
             CREATE TABLE IF NOT EXISTS subsystems (
             subsystem_id SERIAL PRIMARY KEY,
             subsystem_name VARCHAR
             );
             """)
            print("Table ban created or already exists.")
        except Exception as e:
            print("Error while creating table ban:", e)

    async def create_types_of_works_table(self):
        try:
            await self.connection.execute("""
             CREATE TABLE IF NOT EXISTS type_of_works (
             type_of_work_id SERIAL PRIMARY KEY,
             type_of_work_name VARCHAR
             );
             """)
            print("Table ban created or already exists.")
        except Exception as e:
            print("Error while creating table ban:", e)

    async def is_user_banned(self, user_id):
        return await self.connection.fetchval("SELECT user_id FROM banned_users WHERE user_id = $1",
                                              user_id) is not None

    async def ban_user(self, user_id):
        await self.connection.execute("INSERT INTO banned_users (user_id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)

    async def insert_data(self, table_name: str, records_data: Dict[str, Any], conflict_column: Optional[str] = None):
        columns = ', '.join(records_data.keys())
        values = ', '.join(f'${i + 1}' for i in range(len(records_data)))
        values = values.encode('utf-8').decode('utf-8')
        conflict_action = f' ON CONFLICT ({conflict_column}) DO UPDATE SET ' if conflict_column else ''

        query = f"""
            INSERT INTO {table_name} ({columns}) VALUES ({values}){conflict_action}
            RETURNING *;
        """
        try:
            print("Success!")
            return await self.connection.fetch(query, *records_data.values())
        except Exception as e:
            print("Error while inserting data:", e)

    async def get_user_data(self, user_id: int, table_name):
        query = f"SELECT * FROM {table_name} WHERE user_id = $1"
        user_data = await self.connection.fetchrow(query, user_id)
        return user_data

    async def get_keyboard_data(self, user_id: int, table_name='user_keyboard'):
        query = f"SELECT * FROM {table_name} WHERE user_id = $1"
        user_data = await self.connection.fetch(query, user_id)
        return user_data

    async def get_object_data(self):
        query = "SELECT object_name FROM objects"
        user_data = await self.connection.fetch(query)
        return user_data

    async def get_table(self, table_name):
        query = f"SELECT * FROM {table_name}"
        user_data = await self.connection.fetch(query)
        return user_data

    async def count_records(self, table_name):
        query = f"SELECT count(*) FROM {table_name}"
        user_data = await self.connection.fetch(query)
        count = user_data[0][0] if user_data else 0
        return count

    async def count_records_for_certain_user(self, user_id: int, table_name: str) -> int:
        query = f"SELECT count(*) FROM {table_name} WHERE user_id = $1"
        user_data = await self.connection.fetch(query, user_id)
        count = user_data[0][0] if user_data else 0
        return count
    
    async def get_values_data(self, groupp: str):
        query = f"""SELECT object, spent_time FROM records"""
        user_data = await self.connection.fetch(query)
        value = dict(user_data) or {}
        return value

    async def get_users_and_records_tables(self):
        query = """SELECT full_name, object, system, subsystem, spent_time, work_type, date, notes FROM Records r
                    JOIN Users u ON u.user_id = r.user_id;
                    """
        user_data = await self.connection.fetch(query)
        return user_data

    async def get_users_and_notifications_tables(self):
        query = """SELECT full_name, hour, minutes FROM Notifications n
                    JOIN Users u ON u.user_id = n.user_id;
                    """
        user_data = await self.connection.fetch(query)
        return user_data

    async def get_object_names(self):
        query = "SELECT object_name FROM objects"
        user_data = await self.connection.fetch(query)
        return user_data

    async def update_data(self, table_name: str, where_dict: Dict[str, Any], update_dict: Dict[str, Any]):
        set_clause = ', '.join([f"{key} = ${i + 1}" for i, key in enumerate(update_dict.keys())])
        conditions = ' AND '.join([f"{key} = ${i + len(update_dict) + 1}" for i, key in enumerate(where_dict.keys())])

        query = f"""
            UPDATE {table_name}
            SET {set_clause}
            WHERE {conditions};
        """
        try:
            await self.connection.execute(query, *list(update_dict.values()) + list(where_dict.values()))
        except Exception as e:
            print("Error while updating data:", e)

    async def delete_data(self, table_name: str, where_dict: Dict[str, Any]):
        conditions = ' AND '.join([f"{key} = ${i + 1}" for i, key in enumerate(where_dict.keys())])
        query = f"DELETE FROM {table_name} WHERE {conditions};"
        try:
            await self.connection.execute(query, *where_dict.values())
        except Exception as e:
            print("Error while deleting data:", e)

    async def execute_custom_query(self, query: str, *args):
        try:
            return await self.connection.fetch(query, *args)
        except Exception as e:
            print("Error while executing custom query:", e)
