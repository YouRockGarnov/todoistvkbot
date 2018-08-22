from states.Bases.StateBase import StateBase
from states.Bases.AskedState import AskedState
import random

class AutorizedState(StateBase):
    clarifying_questions = [' Все верно?']

    def act(self, data, service):
        message = data['object']['title']
        parsing = self.parse_message(message, service)

        result = self._create_message(parsing)
        if self._need_to_ask(parsing):
            self._next_state = AskedState()
            result += random.choice(AutorizedState.clarifying_questions)
        else:
            self._next_state = self

        self._messages.append(result)

    def parse_message(self, message, service):
        response = {}

        result = self._parse_project()
        response['project'] = result['project']
        message = result['edited_message']

        # TODO добавь проверку есть ли в сообщении дата

        response['task'] = message
        return response

    def _parse_project(self, message: str, service):
        projects = service.get_project_names()

        contexts = ['в {0}', 'В {0}'] # строки, которые могут встретится,
                                        # если пользователь имел ввиду добавить в конкретный проект
        for project in projects:
            inside = [(project, c.format(project)) for c in contexts if c.format(project) in message]
                # понять есть ли контексты с различными проектами в сообщении

            if inside == []:
                return {'project': 'Входящие', 'edited_message': message} # edited_message - сообщение без проекта
            else:
                return {'project': inside[0][0], 'edited_message': message.replace(inside[0][1], '')}

    def _need_to_ask(self, parsing):
        import datetime
        return not (parsing['project'] == 'Входящие' and parsing['date'] == None)

    def _create_message(self, parsing):
        res_message = 'Я добавил {task} '.format(task=parsing['task'])
        res_message += 'в проект {0} '.format(parsing['project'])

        if parsing['date'] != None:
            res_message += 'на {0} '.format(parsing['date'])

        return res_message




