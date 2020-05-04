import os


class BaseConfig(object):
    # SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.getenv('DEBUG', "0")

    AUTODETECT_CPU = os.getenv('AUTODETECT_CPU', "0")
    SERVICE_PORT = os.getenv('SERVICE_PORT', "5000")
    LISTS_PATH = os.getenv('LISTS_PATH', "./lists/")
