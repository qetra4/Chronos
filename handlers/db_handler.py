import asyncpg
from typing import Dict, Any, Optional, List


class PostgresHandler:
    def __init__(self, dsn: str):
        print("Initializing connection to the database with DSN:", dsn)
        self.dsn = dsn

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

    async def get_all_user_ids(self):
        query = "SELECT user_id FROM users;"
        rows = await self.connection.fetch(query)
        user_ids = [row['user_id'] for row in rows]
        return user_ids

    async def create_table_records(self):
        try:
            await self.connection.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    record_id SERIAL PRIMARY KEY,
                    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
                    object TEXT,
                    system TEXT,
                    subsystem TEXT,
                    work_type TEXT,
                    spent_time INT,
                    date DATE,
                    notes VARCHAR(255)
                );
            """)
            print("Table records created or already exists.")
        except Exception as e:
            print("Error while creating table records:", e)

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

    async def is_user_banned(self, user_id):
        return await self.connection.fetchval("SELECT user_id FROM banned_users WHERE user_id = $1",
                                              user_id) is not None

    async def is_user_record_today(self, user_id, today):
        print(user_id, today)
        return await self.connection.fetchval("SELECT record_id FROM records WHERE user_id = $1 AND date = $2",
                                              user_id, today) is not None

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

    async def get_user_data(self, user_id: int, table_name='users_reg'):
        query = f"SELECT * FROM {table_name} WHERE user_id = $1"
        user_data = await self.connection.fetchrow(query, user_id)
        return user_data

    async def get_table(self, table_name):
        query = f"SELECT * FROM {table_name}"
        user_data = await self.connection.fetch(query)
        return user_data

    async def get_both_tables(self):
        query = """SELECT full_name, object, system, spent_time, notes FROM Records r
                    JOIN Users u ON u.user_id = r.user_id;
                    """
        user_data = await self.connection.fetch(query)
        return user_data

    async def select_data(self, table_name: str, where_dict: Optional[Dict[str, Any]] = None,
                          one_dict: bool = False, columns: Optional[List[str]] = None):
        cols = ', '.join(columns) if columns else '*'
        query = f"SELECT {cols} FROM {table_name}"

        if where_dict:
            conditions = ' AND '.join([f"{key} = ${i + 1}" for i, key in enumerate(where_dict.keys())])
            query += f" WHERE {conditions}"

            try:
                result = await self.connection.fetch(query, *where_dict.values())
                return result[0] if one_dict and result else result
            except Exception as e:
                print("Error while selecting data:", e)
        else:
            try:
                return await self.connection.fetch(query)
            except Exception as e:
                print("Error while selecting data:", e)

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
