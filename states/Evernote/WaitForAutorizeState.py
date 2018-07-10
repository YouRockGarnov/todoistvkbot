from states.Evernote.AutorizedState import AutorizedState
from states.Bases.WaitForAutorizeState import WaitForAutorizeState
from tools.log import logger


class EvernoteWaitForAutorizeState(WaitForAutorizeState):
    def __init__(self):
        super().__init__()
        self._success_autoriz_advice = ''
