import os

db_name = "ali.db"
EMAIL_USERNAME = os.getenv("username")
EMAIL_PASSWORD = os.getenv("password")

class config:
    # created by secrets lib in python for test
    SECRET_KEY = 'a15a278b4567a92d8e7ae65c693e7ab7dba8fc01706d68d04d6a14dc9f9c3666'
    WTF_CSRF_SECRET_KEY = "c8bb66efe3a2ade70047b32af1786bb2aebeb31e7ebace965a73a582a025a06d"
    TEMPLATES_AUTO_RELOAD = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class Development(config):
    FLASK_DEBUG = True

class Production(config):
    FLASK_DEBUG = True