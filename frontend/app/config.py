import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = True
