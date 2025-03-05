from aiogram import F
from aiogram.fsm.context import FSMContext
from handlers.states import RegistrationStates
from messages import MESSAGES
from functions.funcs_admin import *
from functions.func_data import *
from aiogram.types import InputFile 

admin_router = Router()
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]


def is_admin(user_id):
    return user_id in admins


@admin_router.message(F.text == "/admin")
async def admin_handler(message: types.Message, state: FSMContext):
    await pg_manager.connect()
    is_user_banned = await pg_manager.is_user_banned(user_id=message.from_user.id)
    if not is_user_banned:
        user_info = await pg_manager.get_user_data(user_id=message.from_user.id, table_name='users')
        if user_info:
            if is_admin(message.from_user.id):
                await message.answer(MESSAGES["admin_choose_option"],
                                     reply_markup=admin_choose_kb(message.from_user.id))
                await state.set_state(RegistrationStates.waiting_for_admin_chose)
            else:
                await message.answer("Недостаточно прав.")
        else:
            await message.answer(MESSAGES['user_pass'])
            await state.set_state(RegistrationStates.waiting_for_password)
    await pg_manager.close()


@admin_router.message(RegistrationStates.waiting_for_admin_chose)
async def admin_choose_handler(message: types.Message, state: FSMContext):
    admin_info = message.text
    await state.update_data(admin_info=admin_info)
    if admin_info == 'Отобрази таблицу':
        await message.answer(MESSAGES['admin_choose_table'], reply_markup=admin_choose_table_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_admin_table)
    elif admin_info == 'Покажи график':
        await message.answer(MESSAGES['what_table'], reply_markup=choose_table_to_show_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_graphic_chose)
    elif admin_info == 'Открой keyboards-редактор':
        await message.answer(MESSAGES['to_whom_edit_kb'], reply_markup=admin_whom_edit_kb(message.from_user.id))
        await state.set_state(RegistrationStates.waiting_for_admin_to_whom_edit_keyboard)


@admin_router.message(RegistrationStates.waiting_for_admin_table)
async def admin_choose_table_handler(message: types.Message, state: FSMContext):
    admin_table = message.text
    await state.update_data(admin_table=admin_table)
    if admin_table == 'Таблица Users':
        await send_table_users(message)
    elif admin_table == 'Таблица Records':
        await send_table_records(message)
    elif admin_table == 'Таблица Banned Users':
        await send_table_banned_users(message)
    elif admin_table == 'Таблица Notifications':
        await send_table_notifications(message)
    elif admin_table == 'Таблица Objects':
        await send_table_objects(message)
    elif admin_table == 'Таблица Systems':
        await send_table_systems(message)
    elif admin_table == 'Таблица Subsystems':
        await send_table_subsystems(message)
    elif admin_table == 'Таблица Types_of_work':
        await send_table_types_of_work(message)


@admin_router.message(RegistrationStates.waiting_for_admin_to_whom_edit_keyboard)
async def admin_to_whom_edit_keyboard_handler(message: types.Message, state: FSMContext):
    whom = message.text
    await state.update_data(whom=whom)
    await message.answer(MESSAGES['admin_how_to_edit_keyboard'],
                         reply_markup=admin_way_to_edit_kb(message.from_user.id))
    await state.set_state(RegistrationStates.waiting_for_way_to_edit_keyboard)


@admin_router.message(RegistrationStates.waiting_for_admin_keyboard_choose)
async def admin_choose_keyboard_handler(message: types.Message, state: FSMContext):
    admin_keyboard = message.text
    await state.update_data(admin_keyboard=admin_keyboard)
    await message.answer(MESSAGES['admin_how_to_edit_keyboard'],
                         reply_markup=admin_way_to_edit_kb(message.from_user.id))
    await state.set_state(RegistrationStates.waiting_for_way_to_edit_keyboard)


@admin_router.message(RegistrationStates.waiting_for_way_to_edit_keyboard)
async def admin_choose_way_handler(message: types.Message, state: FSMContext):
    admin_way = message.text
    await state.update_data(admin_way=admin_way)
    if admin_way == "Удалить кнопку":
        admin_data = await state.get_data()
        admin_keyboard = admin_data.get('admin_keyboard')
        if admin_keyboard == 'Объекты':
            keyboard = await objects_kb(message.from_user.id)
            await state.update_data(field_name='object_name')
            await state.update_data(admin_table='objects')
            await message.answer(MESSAGES['delete_button'], reply_markup=keyboard)
        if admin_keyboard == 'Системы':
            keyboard = await systems_kb(message.from_user.id)
            await state.update_data(field_name='system_name')
            await state.update_data(admin_table='systems')
            await message.answer(MESSAGES['delete_button'], reply_markup=keyboard)
        if admin_keyboard == 'Подсистемы':
            keyboard = await subsystems_kb(message.from_user.id)
            await state.update_data(field_name='subsystem_name')
            await state.update_data(admin_table='subsystems')
            await message.answer(MESSAGES['delete_button'], reply_markup=keyboard)
        if admin_keyboard == 'Тип работы':
            keyboard = await types_of_work_kb(message.from_user.id)
            await state.update_data(field_name='type_of_work_name')
            await state.update_data(admin_table='type_of_works')
            await message.answer(MESSAGES['delete_button'], reply_markup=keyboard)
        await state.set_state(RegistrationStates.waiting_for_delete_button)
    elif admin_way == "Создать кнопку":
        await message.answer(MESSAGES['create_button'], reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(RegistrationStates.waiting_for_create_button)


@admin_router.message(RegistrationStates.waiting_for_create_button)
async def admin_create_button_handler(message: types.Message, state: FSMContext):
    admin_text = message.text
    await state.update_data(admin_text=admin_text)
    await pg_manager.connect()
    admin_data = await state.get_data()
    admin_keyboard = admin_data.get('admin_keyboard')
    try:
        if admin_keyboard == 'Объекты':
            await pg_manager.create_objects_table()
            await pg_manager.insert_data(
                table_name="objects",
                records_data={
                    "object_name": admin_text,
                }
            )

        elif admin_keyboard == 'Системы':
            await pg_manager.create_systems_table()
            await pg_manager.insert_data(
                table_name="systems",
                records_data={
                    "system_name": admin_text,
                }
            )

        elif admin_keyboard == 'Подсистемы':
            await pg_manager.create_subsystems_table()
            await pg_manager.insert_data(
                table_name="subsystems",
                records_data={
                    "subsystem_name": admin_text,
                }
            )

        elif admin_keyboard == 'Тип работы':
            await pg_manager.create_types_of_works_table()
            await pg_manager.insert_data(
                table_name="type_of_works",
                records_data={
                    "type_of_work_name": admin_text,
                }
            )

        await message.answer("Готово!")
    except Exception as e:
        await message.answer(f"Произошла ошибка при сохранении данных: {e}")
    await pg_manager.close()
    await state.clear()


@admin_router.message(RegistrationStates.waiting_for_delete_button)
async def admin_delete_button_handler(message: types.Message, state: FSMContext):
    button = message.text
    user_id = message.from_user.id
    await state.update_data(button=button)
    admin_data = await state.get_data()
    admin_table = admin_data.get('admin_table')
    field_name = admin_data.get('field_name')
    await message.answer("Готово!")
    await pg_manager.connect()
    await pg_manager.delete_data(table_name=admin_table, where_dict={field_name: button})
    await pg_manager.delete_data(table_name='user_keyboard',
                                 where_dict={"user_id": user_id, 'object_name': button})
    await pg_manager.close()
    await state.clear()


@admin_router.message(RegistrationStates.waiting_for_graphic_chose)
async def admin_get_graphic_chose(message: types.Message, state: FSMContext):
    admin_g_chose = message.text
    await state.update_data(admin_g_chose=admin_g_chose)
    await pg_manager.connect()
   
    if admin_g_chose == 'Круговая диаграмма часов работы extra/not extra':
        data_dict = await pg_manager.get_extra_data()
        labels = list(data_dict.keys())
        vals = list(data_dict.values())
        if vals is not None:
            buf = await pie_hours_extra(vals, labels)
    elif admin_g_chose == 'Гистограмма часов работы по объектам':
        data_dict = await pg_manager.get_obj_data()
        labels = list(data_dict.keys())
        vals = list(data_dict.values())
        if vals is not None:
            buf = await hist_hours_by_objects(vals, labels)
    elif admin_g_chose == 'Гистограмма часов работы по системам':
        data_dict = await pg_manager.get_systems_data()
        labels = list(data_dict.keys())
        vals = list(data_dict.values())
        if vals is not None:
            buf = await hist_hours_by_systems(vals, labels)
    elif admin_g_chose == 'Гистограмма часов работы по подсистемам':
        data_dict = await pg_manager.get_subsystems_data()
        labels = list(data_dict.keys())
        vals = list(data_dict.values())
        print(vals, labels)
        if vals is not None:
            buf = await hist_hours_by_subsystems(vals, labels)
    elif admin_g_chose == 'Гистограмма часов работы по типам работ':
        data_dict = await pg_manager.get_types_of_works_data()
        labels = list(data_dict.keys())
        vals = list(data_dict.values())
        if vals is not None:
            buf = await hist_hours_by_types_of_work(vals, labels)

    await state.set_state(RegistrationStates.waiting_for_admin_table)
    if vals is not None:     
        await message.answer_photo(
            photo=types.BufferedInputFile(buf.getvalue(), filename="graph.png"),
            caption='А вот и актуальный график :)',
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await message.answer(MESSAGES['no_info_yet'], reply_markup=types.ReplyKeyboardRemove())
    await pg_manager.close()
    await state.clear()

