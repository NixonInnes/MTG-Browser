class Config(object):
    DATABASE = 'data/mtg.sqlite'
    SERVER_NAME = '127.0.0.1:80'
    DEBUG = False
    SECRET_KEY = 'jniuh9p0yuh*(&Y)7huibni7h07YH&H*87t86g7giob(^T(&^G)*Jooijouh0&Y)*7h'

class Debug(Config):
    DEBUG = True
    SERVER_NAME = '127.0.0.1:8000'
    USERNAME = 'admin'
    PASSWORD = 'default'
