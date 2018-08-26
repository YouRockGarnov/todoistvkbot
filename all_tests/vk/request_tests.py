from tools.debug_process import debug_processing
import vkbot_main
import tools.vkapi as vkapi
from db.mymodels import *
import time
from flask import g
import requests
from tools.log import logger
from todoist import TodoistAPI
from services.TodoistService import TodoistService

main_url = 'https://tattoo-sender.herokuapp.com'
garnovyd_token = '6d8318130bb72124968473a6e269bc3f73cebc0b'
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
              '"user_id": 481116745, "read_state": 0, '
                     '"body": "Привет!"}}')

    debug_processing('{"type": "message_new", '
                     '"object": {"id": 43, "date": 1492522323, "out": 0, '
                     '"user_id": 481116745, "read_state": 0, '
                     '"success": "True"}}')

    acc = Account(login='garnovyd@gmail.com', password='')
    acc.save()

    subs = Subscription(account=acc,
                     messenger=Messenger.get(Messenger.name == 'VK'),
                     subscr_type='free',
                     messenger_user_id=481116745)
    subs.save()

    token = AccessToken(service='Todoist', account=acc, token=garnovyd_token)
    token.save()


def test_add_indox_task():
    g.db.close()
    content = 'Это новая задача!'

    debug_processing('{"type": "message_new", '
              '"object": {"id": 43, "date": 1492522323, "out": 0, '
              '"user_id": 481116745, "read_state": 0, '
                     '"body": "' + content + '"}}')

    acc = Account.get(Account.login == yury_email)

    service = TodoistService()
    api = TodoistAPI(AccessToken.get(account=acc.id).token)
    api.sync()

    found_content = [item['content'] for item in  api.items.all() if item['content'] == content
        and item['project_id'] == service.project_name_to_id(api=api, proj_name='Inbox')][0]

    assertEqual(funcname=test_add_indox_task.__name__, a=found_content, b=content)
    # assertEqual(vkapi.sended_message, 'Я не понял команды. Попробуйте еще раз.', __name__)

    service.delete_task(task=content, proj='Inbox', user_id=481116745)

def test_add_project_task(content, proj_name, task):
    g.db.close()

    debug_processing('{"type": "message_new", '
              '"object": {"id": 43, "date": 1492522323, "out": 0, '
              '"user_id": 481116745, "read_state": 0, '
                     '"body": "' + content + '"}}')

    acc = Account.get(Account.login == yury_email)

    service = TodoistService()
    api = TodoistAPI(AccessToken.get(account=acc.id).token)
    api.sync()

    debug_processing('{"type": "message_new", '
              '"object": {"id": 43, "date": 1492522323, "out": 0, '
              '"user_id": 481116745, "read_state": 0, '
                     '"body": "Ага!"}}')

    api.sync()

    found_content = [item['content'] for item in  api.items.all() if item['content'] == task
        and item['project_id'] == service.project_name_to_id(api=api, proj_name=proj_name)][0]

    assertEqual(funcname=test_add_indox_task.__name__, a=found_content, b=task)
    # assertEqual(vkapi.sended_message, 'Я не понял команды. Попробуйте еще раз.', __name__)

    service.delete_task(task=task, proj=proj_name, user_id=481116745)

def test_add_forwarded_mess():
    service = TodoistService()
    api = service._api_for_user(481116745)
    content = "Это пересланная задача?"

    debug_processing('{"type": "message_new", '
              '"object": {"id": 43,'
              '"user_id": 481116745,'
                     '"body": "", '
                     '"fwd_messages": [{"user_id": 215916134, "date": 1533747040, "body": "Это пересланная задача?"}]}')

    found_content = service.get_task(task_name=content, proj_name='Inbox', user_id=481116745)
    assertEqual(funcname=test_add_indox_task.__name__, a=found_content, b=content)
    # assertEqual(vkapi.sended_message, 'Я не понял команды. Попробуйте еще раз.', __name__)

    service.delete_task(task=content, proj='Inbox', user_id=481116745)