class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'jiskibiwimotiuskabhibaranamhai'
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    SQLALCHEMY_DATABASE_URI  = 'postgresql://postgres:1234@localhost:5432/askprocoders'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI ='postgresql://postgres:1234@localhost:5432/askprocoders'
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False