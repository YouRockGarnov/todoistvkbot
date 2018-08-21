from tools.log import logger
from abc import abstractmethod


class ServiceBase:
    def __init__(self):
        self._email = None

    @abstractmethod
    @staticmethod
    def get_auth_url():
        logger.info('call "get_autorize_url"')
        return 'servicebase url'

    def set_email(self, email):
        self._email = email
        # self._connect_to_service()

    email = property()
    email = email.setter(set_email)
