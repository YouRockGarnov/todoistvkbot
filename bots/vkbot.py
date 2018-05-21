from tools import vkapi
from settings import *
from states.NotAutarizedState import NotAutarizedState
from tools.log import logger


class VKBot:
    def __init__(self):
        self._secretaries = dict()
        self._state = NotAutarizedState()

    def reply_to_message(self, data):
        logger.info('call "vkbot.reply_to_message')
        user_id = data['object']['user_id']

        if user_id not in self._secretaries.keys():
            self._secretaries[user_id] = secretary_type()

        for message in self._secretaries[user_id].reply(data):
            vkapi.send_message(user_id, token, message)

        # Сообщение о том, что обработка прошла успешно
        return 'ok'


def return_all_atr(data):
    mess = list()
    for item in data['object'].values():
        mess.append(item)

    return mess
