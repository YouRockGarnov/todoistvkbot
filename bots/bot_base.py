from settings import *
from tools.log import logger

# Bot обрабатывает сообщения и отправляет их.
# Он один на всю программу для конкретного сервиса (один VKBot и один TelegramBot)
class BotBase:
    def __init__(self):
        self._secretaries = dict() # для каждого пользователя (id) свой секретарь

    def reply_to_message(self, data):
        logger.info('call "bot.reply_to_message')
        user_id = data['object']['user_id']

        # если юзер новый, то создаем ему секретаря
        if user_id not in self._secretaries.keys():
            self._secretaries[user_id] = secretary_type()

        # отправляем все сообщения, которые вернула секретарь
        for message in self._secretaries[user_id].reply(data):
            self.send_message(user_id, message)

        # Сообщение о том, что обработка прошла успешно
        return 'ok'

    # это чисто для BotBase
    from abc import abstractmethod
    @abstractmethod
    def send_message(self, user_id, message):
        logger.info('send \"' + message.encode().decode("utf-8", 'replace') + ' \" to ' + str(user_id))
        print(message)