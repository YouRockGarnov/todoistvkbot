from db.mymodels import *
from flask import Flask, json, request, g
from TodoistVK import app
from db.creating_scratch import create_db
from tools.log import logger
from tools.debug import setDEBUG
from db.creating_scratch import init_db
from db.mymodels import db_proxy

def test():
    with app.app_context():
        init_db()
        g.db = db_proxy
        g.db.connect()

        import all_tests.vk.request_tests as tests

        g.db.drop_tables([Account, Subscription, Messenger, AccessToken])
        create_db()

        tests.test_start()
        tests.test_add_indox_task()
        tests.test_add_project_task(proj_name='Work', content='В Work это новая задача в проекте',
                                    task='это новая задача в проекте')

        tests.test_add_project_task(proj_name='Work', content='Это новая задача в проекте в Work ',
                                    task='Это новая задача в проекте')
        tests.test_add_forwarded_mess()
        tests.test_add_task_with_date()

        logger.info('All tests are passed!')
        return 'ok'

import os
if not ('HEROKU' in os.environ):
    print('unitests started')
    setDEBUG(True)
    test()
    print('unitests ended')