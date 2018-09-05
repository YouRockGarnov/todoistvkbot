from db.mymodels import Subscription, Messenger, Account

def subscribe_to(messenger_name, user_id):
    messenger = Messenger.get(Messenger.name == messenger_name)
    query = Subscription.select().where(Subscription.messenger_user_id == user_id
                                        and Subscription.messenger == messenger)

    if not query.exists():
        acc = Account(login='fakelogin', password='fakepassword')
        acc.save()

        subs = Subscription(account=acc, messenger=Messenger.get(Messenger.name == messenger_name),
                            subscr_type='free', messenger_user_id=user_id)
        subs.save()

