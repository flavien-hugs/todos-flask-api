import os
from dotenv import dotenv_values

env = dotenv_values(".flaskenv")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False

    SECRET_KEY = env.get("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False

    @staticmethod
    def init_app(todos_app):
        pass

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "dev.sqlite3")


class ProdConfig(Config):

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "prod.sqlite3")

    @classmethod
    def init_app(cls, todos_app):
        Config.init_app(todos_app)
        import logging
        from logging.handlers import SysLogHandler

        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        todos_app.logger.addHandler(syslog_handler)


settings = {
    "prod": ProdConfig,
    "dev": DevConfig,
    "test": TestConfig,
}
