from tools import vkapi
from states.StateBase import StateBase


class AutorizedState(StateBase):
    def act(self, data, service):
        messages = list()
        if 'body' in data['object']:
            for message in data['object']['body']:
                messages.append(message['body'])

        service.add_note(messages, data['object']['title'])
        self._messages = ['Я записала эту заметку.']
        self._next_state = AutorizedState()
