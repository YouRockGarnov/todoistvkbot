def _parse_message(message, user_id, service):
    response = {}

    result = _parse_project(message=message, user_id=user_id, service=service)
    response['project'] = result['project']
    message = result['edited_message']

    result = _parse_datetime(message, service, user_id)
    response['date_string'] = result['date_string'] if 'date_string' in result.keys() else ''
    message = result['edited_message']

    response['task'] = message
    return response

def _parse_project(message, service, user_id):
    projects = service.get_project_names(user_id)

    contexts = ['в {0}', 'В {0}']  # строки, которые могут встретится,
    # если пользователь имел ввиду добавить в конкретный проект
    for project in projects:
        inside = [(project, c.format(project)) for c in contexts if c.format(project) in message]
        # понять есть ли контексты с различными проектами в сообщении

        if inside != []:
            edited_message = ''.join([part.strip() for part in message.split(inside[0][1])])
            return {'project': inside[0][0], 'edited_message': edited_message}

    return {'project': 'Inbox', 'edited_message': message}  # edited_message - сообщение без проекта

def _parse_datetime(message, service, user_id):
    weekdays = _inflect(['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'])
    months = _inflect(
        ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь',
         'ноябрь', 'декабрь'])
    short_m = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
    short_w = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    import re


    splited = message.split('.')
    parties = []
    for part in splited:
        parties += part.split(',')

    for part in parties:
        if ('завтра' in part or 'сегодня' in part or 'послезавтра' in part or
                any([day in part for day in weekdays])
                or len(re.compile('((\d{1,2}[ .\/-]\d{1,2})([ .\/-]\d{4})?)').findall(part)) != 0
                or len(re.compile('\d{1,2} чaс[(а)(ов)]').findall(part)) != 0
                or 'на следующей неделе' in part
                or any([month in part for month in months])
                or any([month in part for month in short_m])
                or any([day in part for day in short_w])
                or len(re.findall('\d{1,2}-го', part)) != 0
                or len(re.findall('через \d{1,2}', part)) != 0
                or len(re.findall('\d{1,2} ?[(pm)(am)]', part))):

            message = message.replace('.'+part, '')
            message = message.replace(','+part, '')
            part = part.replace('часов', '')
            return {'date_string': part, 'edited_message': message}

    return {'edited_message': message}

def _inflect(start_words):
    cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']

    import pymorphy2 as pm
    morph = pm.MorphAnalyzer()

    start_words = [morph.parse(word)[0] for word in start_words]
    from itertools import product
    pairs = list(product(start_words, cases))

    return [word.inflect({case})[0] for word, case in pairs]

# def parse_datetime(self, message, service, user_id) -> dict:
#     result = self.parse_date(message, service, user_id)
#     ..
#
# def parse_date(self, message, service, user_id) -> dict:  # return {} or {date: Datetime}
#     from datetime import timedelta, date as dt_date
#     import re
#
#     weekdays = enumerate(
#         ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'])
#
#     date = None
#     time = None
#     if 'завтра' in message:
#         global date
#         date = dt_date.today() + timedelta(1)
#     elif 'сегодня' in message:
#         global date
#         date = dt_date.today()
#     elif 'послезавтра' in message:
#         global date
#         date = dt_date.today() + timedelta(2)
#     elif any([day[1] in message for day in weekdays]):  # если присутствует день недели
#         global date
#         days = [day[0] in message for day in weekdays][0]
#         delta = (dt_date.today().weekday() - days + 7) % 7
#
#         date = dt_date.today() + timedelta(days=delta)
#
#     elif len(re.compile('((\d{1,2}[ .\/-]\d{1,2})([ .\/-]\d{4})?)').findall(
#             message)) != 0:  # если дата указана
#         row_date = re.compile('((\d{1,2}[ .\/-]\d{1,2})([ .\/-]\d{4})?)').findall(message)[0] \
#             .split(' ', '/', '.', '\\', '-')  # находим дату и сплитим по разделителям
#
#         keys = ['day', 'month', 'year']
#         kdate = {}
#         for numb, key in zip(row_date, keys):
#             kdate[key] = numb
#
#         global date
#         if 'year' in kdate.keys():
#             date = dt_date(**kdate)
#         elif 'month' in kdate.keys():
#             date = dt_date(dt_date.today().year, kdate['month'], kdate['day'])
#
#             if date < dt_date.today():
#                 date = date.replace(year=date.year + 1)
#         else:
#             date = dt_date(dt_date.today().year, dt_date.today().month, kdate['day'])
#
#             if date < dt_date.today():
#                 date = date.replace(month=date.month + 1)