import os

# ENV=development or ENV=production
ENV = "development"


EMAIL_USERNAME = os.getenv("username-mail")
EMAIL_PASSWORD = os.getenv("password-mail")
MAIL_PORT = 587


# temp database local
db_username = 'alisharify'
# super secure password :)
db_password = '123654'


if not db_username or not db_password:
    raise RuntimeError("DateBase Username or Password is Not Set/ from config.py set it")


if not EMAIL_USERNAME or not EMAIL_USERNAME:
    raise RuntimeError("Email Username or Password is Not Set/ from config.py set it")

class Config:

    DEFAULT_PICTURE = "default.jpg"
    UPLOAD_FOLDER = "C:\\Users\\alisharify\\Documents\\temp\\Divar.ir\\Python\\divar\\static\\uploads"
    # created by secrets lib in python for test
    SECRET_KEY = 'a15a278b4567a92d8e7ae65c693e7ab7dba8fc01706d68d04d6a14dc9f9c3666'
    WTF_CSRF_SECRET_KEY = "c8bb66efe3a2ade70047b32af1786bb2aebeb31e7ebace965a73a582a025a06d"
    TEMPLATES_AUTO_RELOAD = True
    
    SESSION_PERMANENT = True
    # SESSION_COOKIE_SECURE = True
    SESSION_TYPE = "filesystem"
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_username}:{db_password}@localhost:3306/divar"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    SESSION_COOKIE_SECURE = False
    DEBUG = True


class Production(Config):
    DEBUG = False



