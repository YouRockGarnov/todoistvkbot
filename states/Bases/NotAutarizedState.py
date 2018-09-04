from states.Bases.StateBase import StateBase
from states.Bases.WaitForAutorizeState import WaitForAutorizeState
from abc import abstractstaticmethod
from db.mymodels import Subscription
from db.business_rules import subscribe_to

'''Самое начальное состояние.

'''

class NotAutarizedState(StateBase):
    def __init__(self):
        super().__init__()
        self._mess_ending = '' # что вывести после ссылки.

    def get_default_next_state(self):
        return WaitForAutorizeState()

    def act(self, data, service):
        subscribe_to(data['messenger'], service.name)
        self._messages = ['Рада приветствовать вас. Для продолжения работы необходимо авторизоваться. '
                          'Пройдите по данной ссылке: {0}.\n{1}'.format(service.get_auth_url(), self._mess_ending)]

        self._next_state = self.get_default_next_state()
