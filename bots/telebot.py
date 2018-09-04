from bots.bot_base import BotBase
import configs.config_telebot as config
import telebot

'''Это обертка над оригинальным telebot.

Instance и есть оригинальный.
'''

class Telebot(BotBase):
    def __init__(self):
        super().__init__()
        self._instance = telebot.TeleBot(config.token)

    def send_message(self, user_id, message):
        self._instance.send_message(user_id, message)
