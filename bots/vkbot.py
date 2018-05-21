from bots.bot_base import BotBase
import tools.vkapi


class VKBot(BotBase):
    def __init__(self):
        super().__init__()

    def send_message(self, user_id, token, message):
        vkapi.send_message(user_id, token, message)


def return_all_atr(data):
    mess = list()
    for item in data['object'].values():
        mess.append(item)

    return mess
