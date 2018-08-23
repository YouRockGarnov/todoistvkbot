from db.mymodels import *
from flask import Flask, json, request, g
from app import app
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

        g.db.drop_tables([Account, Subscription, Messenger, AccessToken], safe=True)
        create_db()

        tests.test_start()
        tests.test_add_task()

        logger.info('All tests are passed!')
        return 'ok'

import os
if not ('HEROKU' in os.environ):
    print('unitests started')
    setDEBUG(True)
    test()
    print('unitests ended')