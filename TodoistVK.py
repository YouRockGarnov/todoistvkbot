from flask import Flask, request, json, g
from configs.config_vkbot import *
from settings import *
import tools.debug as debug_module
from bots.vkbot import VKBot
from tools.log import logger, logged
from app import app
from db.creating_scratch import init_db, db_proxy
import db.creating_scratch as creating_scratch

bot = VKBot()

@app.route('/', methods=['GET'])
def describe():
    return 'Это TodoistVKBot!!!'

@app.before_request
@logged
def before_request():
    init_db()
    g.db = db_proxy
    g.db.connect()

@app.after_request
@logged
def after_request(response):
    g.db.close()
    return response

@app.route('/setDEBUG_True', methods=['GET'])
@logged
def setDEBUG_True():
    debug_module.setDEBUG(True)
    return 'DEBUG = True'

@app.route('/setDEBUG_False', methods=['GET'])
@logged
def setDEBUG_False():
    debug_module.setDEBUG(False)
    return 'DEBUG = False'

@app.route('/getDEBUG_Flag', methods=['GET'])
@logged
def get_debug():
    logger.info(debug_module.getDEBUG())
    return 'DEBUG = {0}'.format(debug_module.getDEBUG())


@app.route('/create_db', methods=['GET'])
@logged
def create_db():
    creating_scratch.create_db()
    return 'ok'

@app.route('/reset_db', methods=['GET'])
@logged
def reset_db():
    creating_scratch.reset_db()
    return 'ok'

@app.route('/VK/Todoist', methods=['POST'])
@logged
def processing():
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
        data['messenger'] = Messenger.VK.name

        bot.reply_to_message(data)
        return 'ok'

    return 'ok'

if __name__ == "__main__":
    app.run(host='0.0.0.0') # запускает приложение
