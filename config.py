import os

class Config:
    """basic config"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A0Zr98j/3yXR~XHH!jmN]LWX/,?RT'
    #SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    # send mail
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_ASCII_ATTACHMENTS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'WORK_FROM_HOME API'
    MAIL_PASSWORD =  ''
    FLASKY_MAIL_SUBJECT_PREFIX = ''
    FLASKY_MAIL_SENDER = '2399447849@qq.com'
    FLASKY_ADMIN = '2399447849@qq.com'
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    db_host = 'localhost'
    db_user = ''
    db_pass = ''
    db_name = 'work_from_home'
    '''SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name
    SQLALCHEMY_ECHO=False
    SQLALCHEMY_TRACK_MODIFICATIONS=False'''
    MONGO_URI='mongodb://127.0.0.1:27017/work_from_home'

class TestingConfig(Config):
    
    MONGO_URI='mongodb://127.0.0.1:27017/work_from_home'

class Production(Config):
    MONGO_URI='mongodb://127.0.0.1:27017/work_from_home'
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Production,
    'default': DevelopmentConfig
}

class globle_verable:
    video_path = "/home/fariya/projects/facticss/factics-api-v1.1/app/v1/uploads/recorder/"
