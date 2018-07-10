from states.Evernote.WaitForAutorizeState import WaitForAutorizeState
from states.Bases.NotAutarizedState import NotAutarizedState

# состояния позволяют не делать тысячу ифов, а сделать это в стиле ООП
class EvernoteNotAutarizedState(NotAutarizedState):
    def __init__(self):
        super().__init__()
        self._mess_ending = '\nПришлите ответным письмом email на который вы зарегистрировали аккаунт.'
