from states.Evernote.WaitForAutorizeState import WaitForAutorizeState
from states.Bases.StateBase import StateBase

'''Самое начальное состояние.

'''

class NotAutarizedState(StateBase):
    def __init__(self):
        super().__init__()
        self._mess_ending = '' # что вывести после ссылки.

    def act(self, data, service):
        self._messages = ['Рада приветствовать вас. Для продолжения работы необходимо авторизоваться. '
                          'Пройдите по данной ссылке: {0}.\n{1}'.format(service.get_autorize_url(), self._mess_ending)]

        self._next_state = WaitForAutorizeState()
