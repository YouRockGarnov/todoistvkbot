from bots.telebot import Telebot
from telebot.util import async
import telebot
import configs.config_telebot as config
from settings import *
from tools.debug import *
from tools.log import logger
import time

telegram_bot = Telebot()
bot = telebot.TeleBot(config.token)


@async()
@bot.message_handler(content_types=['text'])
def user_answer(message):
    if DEBUG:
        logger.info('Run in debug')

    data = preparing_message(message)
    logger.info('pulled message: ' + str(data['object']))
    telegram_bot.reply_to_message(data)


def preparing_message(message):
    data = {'object': dict()}
    data['object']['title'] = message.text.split('\n')[0]
    data['object']['body'] = {'body': message.text.split('\n')[1:]}
    data['object']['user_id'] = message.chat.id
    data['object']['success'] = True

    return data


def telebot_main():
    while True:
        try:
            bot.polling(none_stop=True, interval=3)
        except Exception as e:
            # logging.error(e)
            time.sleep(10)


if __name__ == '__main__':
    telebot_main()