from peewee import Model
from peewee import IntegerField
from peewee import ForeignKeyField
from peewee import TextField
from peewee import TextField
from peewee import PostgresqlDatabase, Proxy
from peewee import DateTimeField
from datetime import datetime

db_proxy = Proxy()

class DBModel(Model):
    class Meta:
        database = db_proxy

class Account(Model):
    login = TextField()
    password = TextField()

    class Meta:
        database = db_proxy

class Messenger(Model):
    name = TextField()
    cost = IntegerField()

    class Meta:
        database = db_proxy

class Subscription(Model):
    account = ForeignKeyField(Account, to_field='id', null=True)
    messenger = ForeignKeyField(Messenger, to_field='id')
    subscr_type = TextField() # free, full
    messenger_user_id = IntegerField()

    class Meta:
        database = db_proxy

class AccessToken(Model):
    service = TextField() # Todoist, Evernote, GoogleCalendar
    account = ForeignKeyField(Account, to_field='id')
    token = TextField()

    class Meta:
        database = db_proxy

# class Message(Model):
#     account = ForeignKeyField(Account, backref='id')
#     date_time = DateTimeField()
#     text = TextField()
#
#     class Meta:
#         database = db_proxy