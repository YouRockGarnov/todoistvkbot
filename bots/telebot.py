from bots.bot_base import BotBase
import telebot

class Telebot(BotBase):
    def __init__(self):
        super().__init__()
        self._instance = telebot.TeleBot(config.TOKEN)


