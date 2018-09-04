from configs.config_vkbot import confirmation_token
from db.mymodels import db_proxy
from tools.log import logger, logged
from vkbot_main import bot
import json
import requests
from db.mymodels import Subscription
from flask import g

def debug_processing(strdata):
    print(strdata)

    data = json.loads(strdata)

    db_proxy.connect(True)
    logger.info('in processing')

    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'

    if data['type'] == 'confirmation':
        return confirmation_token

    elif data['type'] == 'message_new' or data['type'] == 'service_reply':
        logger.info('pulled message: ' + str(data['object']))

        bot.reply_to_message(data)
        return 'ok'

    db_proxy.close()
    return 'ok'

# созданно для тестов, чтобы тестить на локальной машине
@logged
def debug_todoist_redirect(args):
    user_id = args['state'] # state по совместительству и user_id, см. TodoistService

    data = {'object': {
        'user_id': user_id,
        'success': 'True'
        }
    }

    from services.TodoistService import TodoistService
    if args['state'] in TodoistService.state_pull:
        try:
            sending_args = {'client_id': 'fb26051eb06649bb968791f3d7c2f185',
                            'client_secret': '9d853dc5aba9490780682f159ff5c611',
                            'code': args['code']}

            response = requests.post('https://todoist.com/oauth/access_token', sending_args)

            import json
            access_token = json.loads(response.text)['access_token']
            subsss = Subscription.get()
            subs = Subscription.select().where(Subscription.messenger_user_id == user_id).get()

            subs.access_token = access_token
            subs.save()

        except Exception as ex:
            import sys
            logger.error(sys.exc_info())
            data['object']['success'] = 'False'

        global bot # предполагается, что vkmain и telemain просто импортируют и там будут свои боты
        bot.reply_to_message(data) # шлем боту сообщение с флагом success