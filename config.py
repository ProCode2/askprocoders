import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = ''
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    SQLALCHEMY_DATABASE_URI  = os.getenv('DATABASE_URL' ,  'postgresql://username: password@localhost/yourdata')

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
