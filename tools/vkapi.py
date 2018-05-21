import vk
from tools.debug import *

def send_message(user_id, token, message, attachment=""):
    if (DEBUG):
        print(message)
    else:
        pass