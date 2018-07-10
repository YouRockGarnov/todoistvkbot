from states.Evernote.WaitForAutorizeState import WaitForAutorizeState
from states.Evernote.StateBase import StateBase

# состояния позволяют не делать тысячу ифов, а сделать это в стиле ООП
class NotAutarizedState(StateBase):
    def act(self, data, service):
        self._messages = ['Рада приветствовать вас. Для продолжения работы необходимо авторизоваться в Evernote. Пройдите по данной ссылке: '
                          + service.get_autorize_url() + '\nПришлите ответным письмом email на который вы зарегистрировали аккаунт.']
        self._next_state = WaitForAutorizeState()
