from states.Evernote.AutorizedState import AutorizedState
from states.Evernote.StateBase import StateBase
from tools.log import logger


class WaitForAutorizeState(StateBase):
    def __init__(self):
        super().__init__()
        self._success_autoriz_advice = ''

    def act(self, data, service):
        logger.info('Call WaitForAutorizationState.act()')

        success = data['object']['success'] # TODO в success должен записываться ответ сервера
        self.email = data['object']['title']

        if success:
            self._messages = ['Авторизация прошла успешно!\n{0}'.format(self._success_autoriz_advice)]
            self._next_state = AutorizedState()

        else:
            self._messages = ['Не получилось авторизоваться! Неверный пароль или логин.']
            self._next_state = self