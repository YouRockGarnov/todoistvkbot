from settings import *
from states.NotAutarizedState import NotAutarizedState
from tools.log import logger
from services.EvernoteService import EvernoteService
from states.WaitForAutorizeState import WaitForAutorizeState


class SecretaryBase:
    def __init__(self):
        self._state = NotAutarizedState()
        self._service = EvernoteService()  # TODO hardcoding, it isn't good
        self._email = None

    def take_off_blouse(self):
        print('rrRRRrr')

    def log_in(self, login, password):
        return self._service.log_in(login, password)

    def reply(self, data):
        user_id = data['object']['user_id']

        self._state.act(data, self._service)

        if type(self._state) == WaitForAutorizeState:
            self._email = self._state.email
            self._service.set_email(self._email)

        messages = self._state._messages
        self._state = self._state.next_state

        for message in messages:
            yield message


