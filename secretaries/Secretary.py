from states.Bases.NotAutarizedState import NotAutarizedState
from services.TodoistService import TodoistService
from services.GCalendarService import GCalendarService
from services.EvernoteService import EvernoteService
from states.Evernote.WaitForAutorizeState import WaitForAutorizeState

# создается для каждого пользователя.
class Secretary:
    def __init__(self, service_type):
        self._service = service_type()
        self._state = self._service.get_start_state()
        self._email = None

    #just for fun
    def take_off_blouse(self):
        print('rrRRRrr')

    def reply(self, data):
        user_id = data['object']['user_id']

        from tools.exceptions import ManualException
        try:
            self._state.act(data, self._service)

            # в этом состоянии должен вернуться емейл
            if type(self._state) == WaitForAutorizeState:
                self._email = self._state.email
                self._service.set_email(self._email)

            messages = self._state._messages
            self._state = self._state.next_state  # заменяем текущее состояние следующим

            for message in messages:
                yield message

        except ManualException as ex:
            yield ex.message



