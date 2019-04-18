import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tH!$isMy$3crEteK3y!'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:cto154@localhost:3306/books'
    SQLALCHEMY_ECHO = True

