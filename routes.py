from app import app
from flask import request
import requests
from flask import g
from db.mymodels import Subscription
from tools.log import logger, logged

@logged
@app.route('/todoist_redirect')
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
                            'client_secret': '',
                            'code': args['code']}

            response = requests.post('https://todoist.com/oauth/access_token', sending_args)
            access_token = response.access_token # TODO
            subs = g.db.get(Subscription.messanger_user_id == user_id)

            subs.access_token = access_token
            subs.save()

        except Exception as ex:
            logger.error(ex.__traceback__)
            data['object']['success'] = 'False'

        global bot # предполагается, что vkmain и telemain просто импортируют и там будут свои боты
        bot.reply_to_message(data) # шлем боту сообщение с флагом success