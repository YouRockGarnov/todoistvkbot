from db.mymodels import Subscription, Messenger

def subscribe_to(messenger, user_id):
    query = Subscription.select().where(Subscription.messenger_user_id == user_id
                                        and Subscription.messenger == messenger)

    if not query.exists():
        subs = Subscription(account=None, messenger=Messenger.get(Messenger.name == messenger),
                            subscr_type='free', messenger_user_id=user_id)
        subs.save()

