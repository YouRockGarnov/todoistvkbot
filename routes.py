from app import app
from flask import request
import requests
from flask import g
from db.mymodels import Subscription

@app.route('/todoist_redirect')
def todoist_redirect():
    args = request.args

    from services.TodoistService import TodoistService
    if args['state'] in TodoistService.state_pull:
        sending_args = {'client_id': 'fb26051eb06649bb968791f3d7c2f185',
                        'client_secret': '',
                        'code': args['code']}

        user_id = args['state']
        response = requests.post('https://todoist.com/oauth/access_token', sending_args)
        access_token = response.access_token # TODO
        subs = g.db.get(Subscription.messanger_user_id == user_id) # state по совместительству и user_id, см. TodoistService

        subs.access_token = access_token
        subs.save()

        data = {'object': {
                'user_id': user_id,
                'success': 'True'
            }
        }

        global bot # предполагается, что vkmain и telemain просто импортируют и там будут свои боты
        bot.reply_to_message(data)