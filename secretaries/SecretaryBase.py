from states.Bases.NotAutarizedState import NotAutarizedState
from services.ServiceBase import ServiceBase
from states.Evernote.WaitForAutorizeState import WaitForAutorizeState

# создается для каждого пользователя.
class SecretaryBase:
    def __init__(self):
        self._state = NotAutarizedState()
        self._service = ServiceBase()
        self._email = None

    #just for fun
    def take_off_blouse(self):
        print('rrRRRrr')

    def reply(self, data):
        user_id = data['object']['user_id']

        self._state.act(data, self._service)

        # в этом состоянии должен вернуться емейл
        if type(self._state) == WaitForAutorizeState:
            self._email = self._state.email
            self._service.set_email(self._email)

        messages = self._state._messages
        self._state = self._state.next_state # заменяем текущее состояние следующим

        for message in messages:
            yield message
