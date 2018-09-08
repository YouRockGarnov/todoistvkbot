
import logging

# create logger with 'spam_application'
logger = logging.getLogger('TodoistVK')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('bot.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

def logged(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info('Enter to function {0}'.format(repr(func)))
            result = func(*args, **kwargs)
            logger.info('Exit from function {0}'.format(repr(func)))
        except Exception as e:
            logger.error("Fatal error in main loop, args: " + args, exc_info=True)

        return result

    return wrapper
