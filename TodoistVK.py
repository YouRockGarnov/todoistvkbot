import requests
from flask import request, json, g, Flask, session

from bots.vkbot import VKBot
from configs.config_vkbot import *
import tools.debug as debug_module
from db.mymodels import Subscription, AccessToken
from tools.log import logger, logged
from db.creating_scratch import init_db, db_proxy
import db.creating_scratch as creating_scratch

app = Flask(__name__)

@app.route('/add_bot', methods=['GET'])
def add_bot():
    session['bot'] = VKBot()
    return '200'

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
    logger.info(g.todoist_state_pull)

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

        session['bot'].reply_to_message(data)
        return 'ok'

    return 'ok'

@app.route('/todoist_redirect', methods=['GET', 'POST'])
@logged
def todoist_redirect():
    args = request.args
    user_id = args['state'] # state по совместительству и user_id, см. TodoistService

    data = {'object': {
        'user_id': user_id,
        'success': 'True'
        }
    }

    # TODO ADD CHECK EXISTANCE OF STATE (МОЖЕТ ЭТО ПОДДЕЛЬНЫЙ ЗАПРОС)

    logger.info(args)
    try:
        sending_args = {'client_id': 'fb26051eb06649bb968791f3d7c2f185',
                        'client_secret': '9d853dc5aba9490780682f159ff5c611',
                        'code': args['code']}

        response = requests.post('https://todoist.com/oauth/access_token', sending_args)

        import json
        str_access_token = json.loads(response.text)['access_token']

        subs = Subscription.get(Subscription.messenger_user_id == user_id)
        acc = subs.account
        access_token = AccessToken(account=acc, token=str_access_token, service='Todoist')
        access_token.save()

    except Exception as ex:
        import sys
        logger.error(sys.exc_info())
        data['object']['success'] = 'False'

      # предполагается, что vkmain и telemain просто импортируют и там будут свои боты
    session['bot'].reply_to_message(data)  # шлем боту сообщение с флагом success

    return '<a href="javascript:close_window();">close</a>'


if __name__ == "__main__":
    app.run(host='0.0.0.0') # запускает приложение