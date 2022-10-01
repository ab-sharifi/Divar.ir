from email.mime import image
from . import config
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_migrate import Migrate

app = Flask(__name__)

if config.ENV == "development":
    app.config.from_object(config.Development)
else:
    app.config.from_object(config.Production)

# mail = Mail(app)
Session(app)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app=app,db=db)

from views.views import *


