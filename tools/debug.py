import functools

'''Если дебаг включен, то бот не будет отсылать сообщения пользователям и взаимодействовать с ними.

Создано для того, чтобы дебажить на локалке.
НИКОГДА НЕ ЗАГРУЖАЙТЕ НА СЕРВЕР С DEBUG = True
'''

DEBUG = True

def getDEBUG():
    global DEBUG
    return DEBUG

def setDEBUG(bool):
    global DEBUG
    DEBUG = bool

# def debug_print_func_name(func):
#     @functools.wraps(func)
#     def wrapped(*args, **kwargs):
#         print(func.__name__)
#
#         return func(*args, **kwargs)
#
#     return wrapped