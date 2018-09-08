from flask import Flask, request, json, g
from configs.config_vkbot import *
from settings import *
import tools.debug as debug_module
from bots.vkbot import VKBot
from tools.log import logger
from app import app
from db.creating_scratch import init_db, db_proxy
import db.creating_scratch as creating_scratch

bot = VKBot()

@app.route('/', methods=['GET'])
def describe():
    return 'Это TodoistVKBot!!!'

@app.before_request
def before_request():
    init_db()
    g.db = db_proxy
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/setDEBUG_True', methods=['GET'])
def setDEBUG_True():
    debug_module.setDEBUG(True)
    return 'DEBUG = True'

@app.route('/setDEBUG_False', methods=['GET'])
def setDEBUG_False():
    debug_module.setDEBUG(False)
    return 'DEBUG = False'

@app.route('/getDEBUG_Flag', methods=['GET'])
def get_debug():
    print(debug_module.getDEBUG())
    return 'DEBUG = {0}'.format(debug_module.getDEBUG())


@app.route('/create_db', methods=['GET'])
def create_db():
    return creating_scratch.create_db()

@app.route('/reset_db', methods=['GET'])
def reset_db():
    return creating_scratch.reset_db()

@app.route('/VK/Todoist', methods=['POST'])
def processing():
    try:
        # Распаковываем json из пришедшего POST-запроса

        logger.info('processing')

        if debug_module.getDEBUG():
            logger.info('Run in debug')

        logger.info(request.data)
        data = json.loads(request.data)
        logger.info(data)

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
    except Exception as e:
        logger.error("Fatal error in main loop", exc_info=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0') # запускает приложение
