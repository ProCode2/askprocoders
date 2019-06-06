class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'jiskibiwimotiuskabhibaranamhai'
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    SQLALCHEMY_DATABASE_URI  = 'postgres://mpwwktyfviknny:845c95a5b9988217222dab1975efa921308abbab8011fdb737e9bc42f164a70e@ec2-107-20-230-70.compute-1.amazonaws.com:5432/d5h0s3qu502euh'

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