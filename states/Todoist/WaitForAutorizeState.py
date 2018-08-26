from states.Todoist.AutorizedState import TodoistAutorizedState
from states.Bases.WaitForAutorizeState import WaitForAutorizeState
from tools.log import logger


class TodoistWaitForAutorizeState(WaitForAutorizeState):
    def __init__(self):
        super().__init__()
        self._success_autoriz_advice = 'Теперь вы можете сохранять задачи, просто переслав сообщения мне! ' \
                                       'Я смогу сама определить какое задание необходимо создать из контекста.'

    def get_default_next_state(self):
        return TodoistAutorizedState()
