class config:
    # created by secrets lib in python for test
    SECRET_KEY = 'a15a278b4567a92d8e7ae65c693e7ab7dba8fc01706d68d04d6a14dc9f9c3666'
    TEMPLATES_AUTO_RELOAD = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_DATABASE_URI = "sqlite:///ali.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MAIL_PORT = 465
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_USERNAME = 'alisharifihashjin@gmail.com'
    # MAIL_PASSWORD = ''
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
class Development(config):
    FLASK_DEBUG = True

class Production(config):
    FLASK_DEBUG = True