
from . import config
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(config.Development)

Session(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


from views.views import *

