from bots.telebot import Telebot
from telebot.util import async
import settings
from tools.debug import *
from tools.log import logger

telegram_bot = Telebot()


@async()
@telegram_bot._instance.message_handler(content_types=['text'])
def user_answer(message):
    if DEBUG:
        logger.info('Run in debug')

    data = preparing_message(message)
    logger.info('pulled message: ' + str(data['object']))
    telegram_bot.reply_to_message(data)


def preparing_message(message):
    data = {'object': dict()}
    data['object']['body'] = message.text
    data['object']['user_id'] = message.chat.id

    return data
