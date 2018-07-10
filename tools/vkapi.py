import vk
from tools.debug import *

session = vk.Session()
api = vk.API(session, v=5.0)

def send_message(user_id, token, message, attachment=""):
    if (DEBUG):
        print(message)
        api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)
    else:
        api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)

def return_all_atr(data):
    mess = list()
    for item in data['object'].values():
        mess.append(item)

    return mess