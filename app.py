from flask import Flask

from bots.vkbot import VKBot

app = Flask(__name__)
bot = VKBot()