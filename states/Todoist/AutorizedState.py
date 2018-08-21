from states.Bases.StateBase import StateBase


class AutorizedState(StateBase):
    def act(self, data, service):
        messages = list()
        if 'body' in data['object']: # взять пересланные сообщения
            for message in data['object']['body']:
                messages.append(message['body'])

        messages.append(data['object']['title'])

        response = service.add_event(messages)

        if response == 'merge':
            self._messages = ['В это время уже есть событие. Я записала ваше поверх этого.']
        else:
            self._messages = ['Я добавила это событие.']
        # TODO добавить вопрос к пользователю о корректности добавления события

        self._next_state = self
