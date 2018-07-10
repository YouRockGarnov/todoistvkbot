from vkbot_main import  debug_processing

def test():
    print(debug_processing({'object': {'user_id': 'user_id', 'body': 'login password'}, 'type': 'message_new'}))
    print(debug_processing({'object': {'user_id': 'user_id', 'success': 'True', 'title': 'hamta@yandex.ru'}, 'type': 'service_reply'}))
    #print(processing({'object': {'user_id': 'user_id', 'title': 'Заголовок', 'body': [{'body': 'Первое пересланное сообщение'},
    #                                                            {'body': 'Второе пересланное сообщение'}]}, 'type': 'message_new'}))
    print(debug_processing({'type': 'message_new', 'object': {'user_id': 'user_id', 'title': 'Title'}}))

test()