import os

db_username = ''
db_password = ''

#  os.getenv("email_username")
#  os.getenv("email_password")

EMAIL_USERNAME = 'temp'
EMAIL_PASSWORD = 'temp'

if not EMAIL_USERNAME or not EMAIL_USERNAME:
    raise ValueError("Email Username or Password is Not Set/ from config.py set it")
if not db_username or not db_password:
    raise ValueError("DateBase Username or Password is Not Set/ from config.py set it")

class Config:
    # created by secrets lib in python for test
    SECRET_KEY = 'a15a278b4567a92d8e7ae65c693e7ab7dba8fc01706d68d04d6a14dc9f9c3666'
    WTF_CSRF_SECRET_KEY = "c8bb66efe3a2ade70047b32af1786bb2aebeb31e7ebace965a73a582a025a06d"
    TEMPLATES_AUTO_RELOAD = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_username}:{db_password}@localhost:3307/divar"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    

class Development(Config):
    SESSION_COOKIE_SECURE = False
    FLASK_DEBUG = True
    DEBUG = True


class Production(Config):
    DEBUG = False
    FLASK_DEBUG = False