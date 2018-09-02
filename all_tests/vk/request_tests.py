from tools.vk_debug_process import debug_processing
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
                     '"fwd_messages": [{"user_id": 215916134, "date": 1533747040, "body": "Это пересланная задача?"}]}}')

    found_content = service.get_task(task_name=content, proj_name='Inbox', user_id=481116745)
    assertEqual(funcname=test_add_indox_task.__name__, a=found_content, b=content)
    # assertEqual(vkapi.sended_message, 'Я не понял команды. Попробуйте еще раз.', __name__)

    service.delete_task(task=content, proj='Inbox', user_id=481116745)

def test_add_task_with_date():
    from time import sleep
    import datetime as dt

    add_task('1', '', 'завтра', 'day', dt.datetime.now() + dt.timedelta(days=1))
    add_task('2', '', 'сегодня в 19 часов', 'hour', )
    add_task('3', 'Work', 'через 3 дня', 'day')
    add_task('4', 'Work', 'на следующей неделе', 'day')
    add_task('5', 'Work', '26/10/2050', 'day')
    add_task('6', '', '3-го', 'day')
    add_task('7', 'Work', 'через 3 часа', 'hour')
    add_task('8', 'Inbox', 'завтра в 18:00', 'hour')
    add_task('9', 'Work', 'в субботу в 15:46', 'hour')
    add_task('10', '', '6 pm', 'hour')

def add_task(task, project='', date_string='', accuracy='day', due_datetime=''):
    g.db.close()

    import time
    time.sleep(1)
    body = '{0}{1}{2}.'.format(task, ' в ' + project if project != '' else '', '. ' + date_string if datetime != '' else '')
    debug_processing('{"type": "message_new", '
              '"object": {"id": 43, "date": 1492522323, "out": 0, '
              '"user_id": 481116745, "read_state": 0, '
                     '"body": "' + body + '"}}')

    time.sleep(1)

    if 'Все верно?' in vkapi.sended_message: # bad
        debug_processing('{"type": "message_new", '
                  '"object": {"id": 43, "date": 1492522323, "out": 0, '
                  '"user_id": 481116745, "read_state": 0, '
                         '"body": "Ага!"}}')

    time.sleep(1)
    acc = Account.get(Account.login == yury_email)

    service = TodoistService()
    api = TodoistAPI(AccessToken.get(account=acc.id).token)
    api.sync()

    project = 'Inbox' if project == '' else project
    try:
        found_content = [item for item in  api.items.all() if item['content'] == task+'.'
            and item['project_id'] == service.project_name_to_id(api=api, proj_name=project)][0]
    except Exception as e:
        print(api.items.all())

        found_content = [item for item in  api.items.all() if item['content'] == task+'.'
            and item['project_id'] == service.project_name_to_id(api=api, proj_name=project)][0]


    assertEqual(funcname=add_task.__name__, a=found_content.data['content'], b=task+'.')

    # import datetime as dt
    # timedelts = {'day': dt.timedelta(days=1), 'hour': dt.timedelta(hours=1)}
    # assertTrue(due_datetime < found_content['due_date_utc'] + timedelts[accuracy]
    #            and due_datetime > found_content['due_date_utc'] - timedelts[accuracy], funcname=add_task.__name__)

    service.delete_task(task=task+'.', proj=project, user_id=481116745)