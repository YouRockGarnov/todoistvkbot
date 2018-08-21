from app import app
from flask import request
import requests

@app.route('/todoist_redirect')
def todoist_redirect():
    args = request.args

    from services.TodoistService import TodoistService
    if args['state'] in TodoistService.state_pull:
        sending_args = {'client_id': 'fb26051eb06649bb968791f3d7c2f185',
                        'client_secret': '',
                        'code': args['code']}

        response = requests.post('https://todoist.com/oauth/access_token', sending_args)
        access_token = response.access_token # TODO
        subs = db.get(Subscription.user_id == args['state']) # state по совместительству и user_id, см. TodoistService

        subs.access_token = access_token
        subs.save()