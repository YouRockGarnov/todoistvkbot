from states.Bases.StateBase import StateBase
from states.Bases.AskedState import AskedState
import random

class TodoistAutorizedState(StateBase):
    clarifying_questions = ['Все верно?']

    def get_default_next_state(self):
        pass
        # return AskedState(TodoistAutorizedState)

    def act(self, data, service):
        message = data['object']['body']
        user_id = data['object']['user_id']
        parsing = self.parse_messages(data, service)
        # parsing = self.parse_fwd_mess(data, service)

        result = self._create_message(parsing)
        if self._need_to_ask(parsing):
            self._next_state = AskedState(TodoistAutorizedState, success_func=service.add_task,
                                          success_data={'content': parsing['task'],
                                                        'project': parsing['project'],
                                                        'date': parsing['date'] if 'date' in parsing.keys() else None,
                                                        'user_id': user_id})
            result +='. '
            result += random.choice(TodoistAutorizedState.clarifying_questions)
        else:
            self._next_state = self
            service.add_task(content=parsing['task'], project=parsing['project'],
                             date=parsing['date'] if 'date' in parsing.keys() else None, user_id=user_id)

        self._messages = [result]


    def parse_messages(self, data, service):
        user_id = data['object']['user_id']
        main_parsing = self._parse_message(data['object']['body'], user_id, service)

        if 'fwd_messages' in data['object']:
            parsing2 = self.parse_date(self._merge_messages(data['object']['fwd_messages']), user_id, service)

            if 'date' not in main_parsing and 'date' in parsing2:
                main_parsing['date'] = parsing2['date']

            main_parsing['task'] = '{0}\n\n{1}'.format(main_parsing['task'], parsing2['task'])

        return main_parsing

    def _parse_message(self, message, user_id, service):
        response = {}

        result = self._parse_project(message=message, user_id=user_id, service=service)
        response['project'] = result['project']
        message = result['edited_message']

        # TODO добавь проверку есть ли в сообщении дата

        response['task'] = message
        return response

    def _parse_project(self, message, service, user_id):
        projects = service.get_project_names(user_id)

        contexts = ['в {0}', 'В {0}'] # строки, которые могут встретится,
                                        # если пользователь имел ввиду добавить в конкретный проект
        for project in projects:
            inside = [(project, c.format(project)) for c in contexts if c.format(project) in message]
                # понять есть ли контексты с различными проектами в сообщении

            if inside != []:
                return {'project': inside[0][0], 'edited_message': message.replace(inside[0][1], '')}

        return {'project': 'Inbox', 'edited_message': message}  # edited_message - сообщение без проекта

    def _need_to_ask(self, parsing):
        import datetime
        return not (parsing['project'] == 'Inbox' and 'date' not in parsing.keys())

    def _create_message(self, parsing):
        res_message = 'Я добавил "{task}" '.format(task=parsing['task'].strip(' '))
        res_message += 'в проект {0}'.format(parsing['project'])

        if 'date' in parsing.keys():
            res_message += 'на {0} '.format(parsing['date'])

        res_message = '{0}.'.format(res_message)
        return res_message

    def _merge_messages(self, messages):
        return messages.join('\n\n')

    def parse_datetime(self, message, service, user_id) -> dict:
        weekdays = enumerate(self.['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'])
        months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
        import re

        if ('завтра' in message or 'сегодня' in message or 'послезавтра' in message or
            any([day[1] in message for day in weekdays])
            or len(re.compile('((\d{1,2}[ .\/-]\d{1,2})([ .\/-]\d{4})?)').findall(message)) != 0
            or len(re.compile('\d{1,2} час[а, ов]').findall(message)) != 0)

    def inflect(self, start_words):
        cases = ['gent', 'datv', 'accs', 'ablt', 'loct']

        import pymorphy2 as pm
        morph = pm.MorphAnalyzer()

        start_words = [morph.parse(word) for word in start_words]
        from itertools import product
        pairs = product(start_words, cases)

        return [word.inflect({case}) for word, case in pairs]









