from . import config
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# print(app.config["FLASK_DEBUG"])

if app.config["ENV"] == "development":
    app.config.from_object(config.Development)
else:
    app.config.from_object(config.Production)


Session(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


from views.views import *

