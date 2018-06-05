import os


# basedir = os.path.abspath(os.path.dirname(__file__))
#
# class Config:
#     SECRET_KEY = os.environ.get('SECRECT_KEY') or 'hard to guess string'
#     SQLALCHEMY_COMMIT_ON_TEARDOWN = True
#
#     @staticmethod
#     def init_app(app):
#         pass
#
#
# class ProductionConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/tushare?charset=utf8'
#
#
#
# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI =  'mysql+pymysql://root:root@127.0.0.1/tushare?charset=utf8'
#
# config = {
#     'testing': TestingConfig,
#     'production': ProductionConfig,
#     'default': TestingConfig
# }



class objectServer(object):
    '''All requests into this app'URL will be reidirected to the server IP'''
    object_server_IP = 'http://172.16.116.136:7086'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'HardToSay1'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class MacConfig(Config):
    # Mac mysql
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:adadad1@127.0.0.1:3306/mock?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ent_all:ent@172.16.117.226:3306/ent_portal?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'mysql://root:adadad1@127.0.0.1:3306/mock'
    SQLALCHEMY_BINDS = {
        # 'mock_data': 'mysql+pymysql://root:adadad1@127.0.0.1:3306/mock?charset=utf8',
        'mysql_117.226': 'mysql+pymysql://ent_all:ent@172.16.117.226:3306/ent_portal?charset=utf8'
    }


class TestingConfig(Config):
    DEBUG = True
    # old config:
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/tushare?charset=utf8'
    # mac mysql
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:adadad1@localhost/sdauto?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://alimysql:alimysql7933@47.98.133.163/mock?charset=utf8'
    SQLALCHEMY_BINDS = {
        # 'mock_data': 'mysql+pymysql://root:adadad1@127.0.0.1:3306/mock?charset=utf8',
        # 'mysql_117.226': 'mysql+pymysql://ent_all:ent@172.16.117.226:3306/ent_portal?charset=utf8'
    }
    SQLALCHEMY_ECHO = True  # set sql echo = true


configs = {
    'mac': MacConfig,
    'default': TestingConfig
}
