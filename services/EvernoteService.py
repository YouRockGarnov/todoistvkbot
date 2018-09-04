from services.ServiceBase import ServiceBase
from tools.log import logger
import requests
import json


class EvernoteService(ServiceBase):
    def add_note(self, messages, title): # old method
        text = str()
        for message in messages:
            text += message

        logger.info('call "add_note"')
        response = requests.post('https://tremendousmajesticform--shibaeff.repl.co/message/', json=json.dumps({'title': title, 'messages': text, 'email': self._email}))

        return response.text
