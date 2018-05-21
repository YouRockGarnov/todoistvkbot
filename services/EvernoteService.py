from services.ServiceBase import ServiceBase
from tools.log import logger
import requests
import json


class EvernoteService(ServiceBase):
    def add_note(self, messages, title):
        text = str()
        for message in messages:
            text += message

        logger.info('call "add_note"')
        requests.post('post.com', json=json.dumps({'title': title, 'messages': text, 'email': self._email}))

    def set_email(self, email):
        self._email = email