from handlers.handler_db import PostgresHandler

async def database_open( pg_manager: PostgresHandler):
    await pg_manager.connect()
    await pg_manager.create_table_users()
    await pg_manager.create_ban_table()
    await pg_manager.create_notifications_table()
    await pg_manager.create_objects_table()
    await pg_manager.create_systems_table()
    await pg_manager.create_subsystems_table()
    await pg_manager.create_types_of_works_table()
    await pg_manager.create_c_types_of_works_table()
    await pg_manager.create_c_systems_table()
    await pg_manager.create_user_keyboard_table()
    await pg_manager.create_table_records()
    await pg_manager.close()
