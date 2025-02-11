from aiogram.fsm.context import FSMContext
from keyboards import *
from datetime import timedelta


async def write_notes_handler(user_id: int, state: FSMContext):
    user_data = await state.get_data()
    user_date = user_data.get('user_date')
    today = user_data.get('user_today')
    user_object = user_data.get('user_object')
    user_system = user_data.get('user_system')
    user_subsystem = user_data.get('user_subsystem')
    user_type_of_work = user_data.get('user_type_of_work')
    user_extra = user_data.get('user_extra')
    user_spent_time = user_data.get('user_spent_time')
    user_till_date = user_data.get('user_till_date')    
    user_notes = user_data.get('user_notes')    
    
    await pg_manager.connect()
    await pg_manager.create_table_records()
    
    if user_date is None:
        user_date = today
        
    if user_till_date:
        dates = []
        current_date = today
        while current_date <= user_till_date:
            if current_date.weekday() < 5:
                dates.append(current_date)
            current_date += timedelta(days=1)
    else:
        dates = [user_date]
        
    try:
        for record_date in dates:
            await pg_manager.insert_data(
                table_name='records',
                records_data={
                    "user_id": user_id,
                    "object": user_object,
                    "system": user_system,
                    "subsystem": user_subsystem,
                    "work_type": user_type_of_work,
                    "spent_time": user_spent_time,
                    "extra": user_extra,
                    "date": record_date,
                    "notes": user_notes
                }
            )

    except Exception as e:
        print(f"Произошла ошибка при сохранении данных: {e}")
        return None
