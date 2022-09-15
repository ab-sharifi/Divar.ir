import os

from pymysql import DBAPISet
from . import config
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect,CSRFError

app = Flask(__name__)
app.config.from_object(config.Development)

Session(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


from views.views import *

# if config.db_name not in os.listdir(): 
#     db.create_all()

# if __name__ == '__main__':
#     app.run(host="0.0.0.0",debug=True,port=8080)


if __name__ == '__main__':
    app.run(host="0.0.0.0",
    debug=config.Development.FLASK_DEBUG,
    port=8080)