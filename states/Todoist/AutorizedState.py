from states.Bases.StateBase import StateBase
from states.Bases.AskedState import AskedState
import random
from parsers import TodoistParser

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
                                                        'date_string': parsing['date_string'] if 'date_string' in parsing.keys() else None,
                                                        'user_id': user_id})
            result += '. ' if result[len(result)-1] != '.' else ' '
            result += random.choice(TodoistAutorizedState.clarifying_questions)
        else:
            self._next_state = self
            service.add_task(content=parsing['task'], project=parsing['project'],
                             date_string=parsing['date_string'] if 'date_string' in parsing.keys() else None, user_id=user_id)

        self._messages = [result]


    def parse_messages(self, data, service):
        user_id = data['object']['user_id']
        main_parsing = TodoistParser._parse_message(data['object']['body'], user_id, service)

        if 'fwd_messages' in data['object']:
            parsing2 = TodoistParser._parse_message(self._merge_messages(data['object']['fwd_messages']), user_id, service)

            if 'date_string' not in main_parsing and 'date_string' in parsing2:
                main_parsing['date_string'] = parsing2['date_string']

            main_parsing['task'] = '{0}\n\n{1}'\
                .format(main_parsing['task'], parsing2['task']) if main_parsing['task'] != '' \
                else parsing2['task']

        return main_parsing

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
        return '\n\n'.join([message['body'] for message in messages])











