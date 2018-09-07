from flask import Flask, request, json
from configs.config_vkbot import *
from settings import *
from tools.debug import *
from bots.vkbot import VKBot
from tools.log import logger
from app import app

bot = VKBot()

@app.route('/', methods=['GET'])
def describe():
    return 'Это TodoistVKBot'

@app.route('/VK/Todoist', methods=['POST'])
def processing():
    # Распаковываем json из пришедшего POST-запроса

    logger.info('processing')

    if DEBUG:
        logger.info('Run in debug')

    data = json.loads(request.data)

    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'

    if data['type'] == 'confirmation':
        return confirmation_token

    elif data['type'] == 'message_new' or data['type'] == 'service_reply':
        logger.info('pulled message: ' + str(data['object']))

        from tools.constants import Messenger
        data['messenger'] = Messenger.VK

        bot.reply_to_message(data)
        return 'ok'

    return 'ok'

if __name__ == "__main__":
    app.run(host='0.0.0.0') # запускает приложение
