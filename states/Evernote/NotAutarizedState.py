from states.Evernote.WaitForAutorizeState import WaitForAutorizeState
from states.Evernote.StateBase import StateBase

# состояния позволяют не делать тысячу ифов, а сделать это в стиле ООП
class NotAutarizedState(StateBase):
    def __init__(self):
        super.__init__()
        self._mess_ending = '\nПришлите ответным письмом email на который вы зарегистрировали аккаунт.'
