import os

db_username = ''
db_password = ''

#  os.getenv("email_username")
#  os.getenv("email_password")

EMAIL_USERNAME = ''
EMAIL_PASSWORD = ''
MAIL_PORT = 587

if not EMAIL_USERNAME or not EMAIL_USERNAME:
    raise RuntimeError("Email Username or Password is Not Set/ from config.py set it")
if not db_username or not db_password:
    raise RuntimeError("DateBase Username or Password is Not Set/ from config.py set it")

class Config:
    # created by secrets lib in python for test
    SECRET_KEY = 'a15a278b4567a92d8e7ae65c693e7ab7dba8fc01706d68d04d6a14dc9f9c3666'
    WTF_CSRF_SECRET_KEY = "c8bb66efe3a2ade70047b32af1786bb2aebeb31e7ebace965a73a582a025a06d"
    TEMPLATES_AUTO_RELOAD = True
    
    SESSION_PERMANENT = False
    SESSION_COOKIE_SECURE = True
    SESSION_TYPE = "filesystem"
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_username}:{db_password}@localhost:3307/divar"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail configuration
    # MAIL_SERVER = ""
    # MAIL_USERNAME = ""
    # MAIL_PASSWORD = ""
    # MAIL_PORT = 25
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = False
    # MAIL_DEBUG = True
    

class Development(Config):
    SESSION_COOKIE_SECURE = False
    FLASK_DEBUG = True
    DEBUG = True


class Production(Config):
    DEBUG = False
    FLASK_DEBUG = False
