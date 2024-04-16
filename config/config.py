import os
from sqlalchemy import URL

app_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

    MAIL_SERVER = None
    MAIL_PORT = None
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'YOU_MAIL@mail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'password')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = URL.create(
        os.environ.get('DIALECT'),
        username=os.environ.get('USERNAME'),
        password=os.environ.get('PASSWORD'),
        host=os.environ.get('HOST'),
        port=os.environ.get('PORT'),
        database=os.environ.get('DB_NAME')
        )


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        app_dir, 'flask_boilerplate_test.db'
        )
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
