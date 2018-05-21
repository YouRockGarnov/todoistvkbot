# from states.NotAutarizedState import NotAutarizedState

class StateBase:
    def __init__(self):
        self._messages = ['Простите, у меня возникли непредвиденные проблемы. Попробуйте позже или обратитесь за помощью к сообществу ']
        self._next_state = None

    @property
    def messages(self):
        return self._messages

    @property
    def next_state(self):
        return self._next_state
