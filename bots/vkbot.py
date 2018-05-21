from bots.bot_base import BotBase
import configs.config_vkbot as config
import tools.vkapi


class VKBot(BotBase):
    def __init__(self):
        super().__init__()

    def send_message(self, user_id, message):
        vkapi.send_message(user_id, config.token, message)


def return_all_atr(data):
    mess = list()
    for item in data['object'].values():
        mess.append(item)

    return mess
