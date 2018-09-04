from tools.log import logger
from abc import abstractstaticmethod
import abc


class ServiceBase:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._email = None
        self._name = None

    @abstractstaticmethod
    def get_auth_url():
        logger.info('call "get_autorize_url"')
        return 'servicebase url'

    def set_email(self, email):
        self._email = email
        # self._connect_to_service()

    @property
    def name(self):
        return self._name

    email = property()
    email = email.setter(set_email)
