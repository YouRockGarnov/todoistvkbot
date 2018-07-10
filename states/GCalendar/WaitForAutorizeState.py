from states.Evernote.AutorizedState import AutorizedState
from states.Bases.WaitForAutorizeState import WaitForAutorizeState
from tools.log import logger


class GCalWaitForAutorizeState(WaitForAutorizeState):
    def __init__(self):
        super().__init__()
        self._success_autoriz_advice = 'Теперь вы можете сохранять события, просто переслав сообщения мне! ' \
                                       'Я смогу сама определить какое событие необходимо создать из контекста.'
