from tools.debug_process import debug_processing
import vkbot_main
import tools.vkapi as vkapi
from db.mymodels import *
import time
from flask import g
import requests
from tools.log import logger
from pytodoist.api import TodoistAPI

main_url = 'https://tattoo-sender.herokuapp.com'
garnovyd_token = '98a4ba5432236a12f235d457db76c7f4dc0865ed'
yury_email = 'garnovyd@gmail.com'

def assertTrue(expr, funcname):
    if not expr:
        print('!! Not true in {0} !!!'.format(funcname))
        exit(1)

def assertEqual(a, b, funcname):
    if a != b:
        print('{0} != {1} in {2}!'.format(a, b, funcname))
        exit(1)

def make_req(message):
    response = requests.post(main_url, message.encode())

    if response != 200:
        logger.error('POST request to {0} with message = {1} returned {2}.'.format(main_url, message, response))
        exit(1)

def test_start():
    g.db.close()

    debug_processing('{"type": "message_new", '
              '"object": {"id": 43, "date": 1492522323, "out": 0, '
              '"user_id": 142872618, "read_state": 0, '
                     '"body": "Привет!"}}')

    acc = Account(login='garnovyd@gmail.com', password='passwordlol')
    acc.save()

    subs = Subscription(account=acc,
                     messenger=Messenger.get(Messenger.name == 'VK'),
                     subscr_type='free',
                     messenger_user_id=481116745)
    subs.save()

    token = AccessToken(service='Todoist', account=acc, token=garnovyd_token)
    token.save()


def test_add_task():
    g.db.close()
    content = 'Это новая задача!'

    debug_processing('{"type": "message_new", '
              '"object": {"id": 43, "date": 1492522323, "out": 0, '
              '"user_id": 142872618, "read_state": 0, '
                     '"body": "' + content + '"}}')

    api = TodoistAPI()
    acc = Account.get(Account.login == yury_email)
    user = api.login_with_google(yury_email, AccessToken.get(acc=acc).token)
    project = user.get_project('Inbox')
    tasks = project.get_tasks()

    contents = [task.content for task in tasks]
    assertTrue(content in contents)
    # assertEqual(vkapi.sended_message, 'Я не понял команды. Попробуйте еще раз.', __name__)
