from states.Bases.StateBase import StateBase
from tools.log import logger
from abc import abstractmethod

class WaitForAutorizeState(StateBase):
    def __init__(self):
        super().__init__()
        self._success_autoriz_advice = ''

    @abstractmethod
    @staticmethod
    def AutorizedState():
        # должен возвращать авторизированное состояние
        pass

    def act(self, data, service):
        logger.info('Call WaitForAutorizationState.act()')

        success = data['object']['success'] # TODO в success должен записываться ответ сервера
        # self.email = data['object']['title']

        if success == 'True':
            self._messages = ['Авторизация прошла успешно!\n{0}'.format(self._success_autoriz_advice)]
            self._next_state = self.AutorizedState()

        else:
            self._messages = ['Не получилось авторизоваться! Неверный пароль или логин.']
            self._next_state = self
