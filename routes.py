from app import app
from flask import request
import requests
from flask import g
from db.mymodels import Subscription, AccessToken
from tools.log import logger, logged

@app.route('/todoist_redirect')
@logged
def todoist_redirect():
    args = request.args
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
            str_access_token = json.loads(response.text)['access_token']

            subs = Subscription.get(Subscription.messenger_user_id == user_id)
            acc = subs.account
            access_token = AccessToken(account=acc, token=str_access_token, service='Todoist')
            access_token.save()

        except Exception as ex:
            import sys
            logger.error(sys.exc_info())
            data['object']['success'] = 'False'

        global bot  # предполагается, что vkmain и telemain просто импортируют и там будут свои боты
        bot.reply_to_message(data)  # шлем боту сообщение с флагом success