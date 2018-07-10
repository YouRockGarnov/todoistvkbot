from states.Evernote.WaitForAutorizeState import WaitForAutorizeState
from states.Evernote.StateBase import StateBase

# состояния позволяют не делать тысячу ифов, а сделать это в стиле ООП
class NotAutarizedState(StateBase):
    def __init__(self):
        super().__init__()
        self._mess_ending = ''

    def act(self, data, service):
        self._messages = ['Рада приветствовать вас. Для продолжения работы необходимо авторизоваться. '
                          'Пройдите по данной ссылке: {0}.\n{1}'.format(service.get_autorize_url(), self._mess_ending)]

        self._next_state = WaitForAutorizeState()