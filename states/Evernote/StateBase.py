from tools.log import logger

class StateBase:
    def __init__(self):
        logger.info('StateBase.__init__()')
        self._messages = ['Простите, у меня возникли непредвиденные проблемы. Попробуйте позже или обратитесь за помощью к сообществу ']
        self._next_state = None

    # какие сообщения возвращает state после act(). Можно было бы просто в act() возвращать json, но это не гибко.
    @property
    def messages(self):
        return self._messages

    # какое следующее состояние
    @property
    def next_state(self):
        return self._next_state
