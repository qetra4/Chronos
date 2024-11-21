know_name = '''
Итак, начнем. Я - Хронос, бот, собирающий статистические данные о времени, которое затрачивается на те или иные виды работ. 
Познакомимся? Напиши своё имя и фамилию.
'''

know_role = '''
Здорово! Теперь выбери свою специальность из предложенных:
'''

hello = '''
Привет-привет!
'''

know_object = '''
На каком объекте ты сегодня работал?
'''

know_system = '''
Какую систему обслуживал?
'''

know_subsystem = '''
Что это была за подсистема?
'''

know_type_of_work = '''
Что за работу выполнял?
'''

know_spent_time = '''
Сколько часов на нее ушло? Напиши ответ одним целым числом
'''

know_notes = '''
Есть ли какие-то комментарии к проделанной работе? Если нет, отправь прочерк.
'''

know_more = '''
Работал ли еще над чем-нибудь сегодня?
'''

goodbye = '''
Замечательно, я всё записал. Спасибо за уделенное время!
'''

user_pass = '''
Привет! Чтобы начать работу, необходимо ввести пароль.
'''

wrong_answer = '''
Пароль неверный. Попробуйте еще раз.
'''

banned_message = '''
Вы заблокированы за превышение попыток ввода пароля. Для разблокировки обратитесь к веб-девелоперу комании.
'''

intention_message = '''
Расскажешь, что делал сегодня? Можешь отказаться и заполнить позже, тогда нужно будет только указать причину, почему.
'''

why_not = '''
Собственно, почему? Опиши вкратце.
'''

notifications_time = '''
Здесь ты можешь установить удобное время для напоминалок от меня.
Вначале я попрошу указать тебя час в пределах 0-23, потом минуты в пределах 0-59. 
То есть, чтобы поставить уведомления на 12:05, нужно вначале отправить 12, затем 5.
Итак, пиши час.
'''

got_hours = '''
Отлично. Теперь вводи минуты
'''

value_error = '''
Вводи числовое значение -_-
'''

diaposon_error_hours = '''
Час должен быть в пределах 0-23 -_-
'''

diaposon_error_minutes = '''
Минуты должны быть в пределах 0-59 -_-
'''

admin_choose_option = '''
Привет, Стас :) Что мне для тебя сделать?
'''

admin_choose_table = '''
Какая таблица тебя интересует?
'''

admin_choose_keyboard = '''
Какую из клавиатур будем редактировать?
'''

admin_how_to_edit_keyboard = '''
Что нужно сделать?
'''

delete_button = '''
Нажми на кнопку, которую хочешь удалить
'''

create_button = '''
Напиши название новой кнопки
'''

same_object = '''
Работал на том же объекте?
'''


MESSAGES = {
    'know_name': know_name,
    'know_role': know_role,
    'hello': hello,
    'know_object': know_object,
    'know_system': know_system,
    'know_spent_time': know_spent_time,
    'know_subsystem': know_subsystem,
    'know_type_of_work': know_type_of_work,
    'know_notes': know_notes,
    'know_more': know_more,
    'goodbye': goodbye,
    'user_pass': user_pass,
    'wrong_answer': wrong_answer,
    'banned_message': banned_message,
    'intention_message': intention_message,
    'why_not': why_not,
    'notifications_time': notifications_time,
    'got_hours': got_hours,
    'value_error': value_error,
    'diaposon_error_hours': diaposon_error_hours,
    'diaposon_error_minutes': diaposon_error_minutes,
    'admin_choose_option': admin_choose_option,
    'admin_choose_table': admin_choose_table,
    'admin_choose_keyboard': admin_choose_keyboard,
    'admin_how_to_edit_keyboard': admin_how_to_edit_keyboard,
    'delete_button': delete_button,
    'create_button': create_button,
    'same_object': same_object,
}
