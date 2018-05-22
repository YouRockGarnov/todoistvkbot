from states.WaitForAutorizeState import WaitForAutorizeState
from states.StateBase import StateBase
from tools import vkapi


class NotAutarizedState(StateBase):
    def act(self, data, service):
        self._messages = ['Рада приветствовать вас. Для продолжения работы необходимо авторизоваться в Evernote. Пройдите по данной ссылке: '
                          + service.get_autorize_url() + '\nПришлите ответным письмом email на который вы зарегистрировали аккаунт.']
        self._next_state = WaitForAutorizeState()
