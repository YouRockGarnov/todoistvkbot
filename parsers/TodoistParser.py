

class TodoistParser:
    def parse_datetime(self, message, service, user_id) -> dict:
        result = self.parse_date(message, service, user_id)
        ..

    def parse_date(self, message, service, user_id) ->  dict: # return {} or {date: Datetime}
        from datetime import timedelta, date as dt_date
        import re

        weekdays = enumerate(['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'])

        date = None
        time = None
        # TODO refactor it
        if 'завтра' in message:
            global date
            date = dt_date.today() + timedelta(1)
        elif 'сегодня' in message:
            global date
            date = dt_date.today()
        elif 'послезавтра' in message:
            global date
            date = dt_date.today() + timedelta(2)
        elif any([day[1] in message for day in weekdays]): # если присутствует день недели
            global date
            days = [day[0] in message for day in weekdays][0]
            delta = (dt_date.today().weekday() - days + 7) % 7

            date = dt_date.today() + timedelta(days=delta)

        elif len(re.compile('((\d{1,2}[ .\/-]\d{1,2})([ .\/-]\d{4})?)').findall(message)) != 0: # если дата указана
            row_date = re.compile('((\d{1,2}[ .\/-]\d{1,2})([ .\/-]\d{4})?)').findall(message)[0]\
                .split(' ', '/', '.', '\\', '-') # находим дату и сплитим по разделителям


            keys = ['day', 'month', 'year']
            kdate = {}
            for numb, key in zip(row_date, keys):
                kdate[key] = numb

            global date
            if 'year' in kdate.keys():
                date = dt_date(**kdate)
            elif 'month' in kdate.keys():
                date = dt_date(dt_date.today().year, kdate['month'], kdate['day'])

                if date < dt_date.today():
                    date = date.replace(year=date.year + 1)
            else:
                date = dt_date(dt_date.today().year, dt_date.today().month, kdate['day'])

                if date < dt_date.today():
                    date = date.replace(month=date.month + 1)