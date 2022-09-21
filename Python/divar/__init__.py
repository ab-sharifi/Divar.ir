from email.mime import image
from . import config
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

app = Flask(__name__)
# print(app.config["FLASK_DEBUG"])

if app.config["ENV"] == "development":
    app.config.from_object(config.Development)
else:
    app.config.from_object(config.Production)

mail = Mail(app)

Session(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


from views.views import *


from .forms import UserUpload
import uuid
from .models import User





