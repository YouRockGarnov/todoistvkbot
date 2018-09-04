from tools.log import logger
from abc import ABCMeta, abstractmethod

'''Состояния - инструмент для секретарей, реализующие логику работы.

Для каждого типа секретаря свои состояния.
Cостояния позволяют не делать тысячу ифов, а сделать это в стиле ООП.
'''
class StateBase(metaclass=ABCMeta):
    def __init__(self):
        logger.info('StateBase.__init__()')
        self._messages = ['Простите, у меня возникли непредвиденные проблемы. '
                          'Попробуйте позже или обратитесь за помощью к сообществу ']
                        # лучше пусть будет так по дефолту, чтобы бот не молчал и дебажить легче было бы

        self._next_state = self.get_default_next_state()

    # какие сообщения возвращает state после act(). Можно было бы просто в act() возвращать json, но это не гибко.
    @property
    def messages(self):
        return self._messages

    # чтобы не было тупых ошибок - если не реализовать - заругается
    @abstractmethod
    def get_default_next_state(self):
        pass

    # какое следующее состояние
    @property
    def next_state(self):
        return self._next_state
