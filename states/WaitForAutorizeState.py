from states.AutorizedState import AutorizedState
from states.StateBase import StateBase
from tools import vkapi
from tools.log import logger


class WaitForAutorizeState(StateBase):
    def act(self, data, service):
        logger.info('Call WaitForAutorizationState.act()')

        success = data['object']['success']
        self.email = data['object']['title']

        if success:
            self._messages = ['Авторизация прошла успешно! '
                                            'Теперь вы можете сохранять заметки, просто переслав сообщения мне!']
            self._next_state = AutorizedState()

        else:
            self._messages = ['Не получилось авторизоваться! Неверный пароль или логин.']
            self._next_state = self
