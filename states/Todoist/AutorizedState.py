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
        parsing = self.parse_message(data, service)

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

    def parse_message(self, data, service):
        response = {}
        message = data['object']['body']
        user_id = data['object']['user_id']

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

        return res_message




