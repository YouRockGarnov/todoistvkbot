from tools.log import logger


class ServiceBase:
    def __init__(self):
        self._email = None

    def get_autorize_url(self):
        logger.info('call "get_autozie_url"')
        return 'http://tremendousmajesticform--shibaeff.repl.co/'

    def set_email(self, email):
        self._email = email
        self._connect_to_service()

    email = property()
    email = email.setter(set_email())
