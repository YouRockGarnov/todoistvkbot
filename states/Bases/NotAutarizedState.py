from states.Bases.StateBase import StateBase
from states.Bases.WaitForAutorizeState import WaitForAutorizeState
from abc import abstractstaticmethod

# состояния позволяют не делать тысячу ифов, а сделать это в стиле ООП
class NotAutarizedState(StateBase):
    def __init__(self):
        super().__init__()
        self._mess_ending = ''

    @abstractstaticmethod
    def WaitForAutorizeState():
        return WaitForAutorizeState()

    def get_default_next_state(self):
        return self.WaitForAutorizeState()

    def act(self, data, service):
        self._messages = ['Рада приветствовать вас. Для продолжения работы необходимо авторизоваться. '
                          'Пройдите по данной ссылке: {0}.\n{1}'.format(service.get_auth_url(), self._mess_ending)]

        self._next_state = self.WaitForAutorizeState()
