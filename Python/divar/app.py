# this is a pseudo base flask app  
# but the actually flask app located in app module(base_app.py)

from divar import config
from flask import Flask
from flask_session import Session

app = Flask(__name__)
Session(app)

# web app config loaded
app.config.from_object(config.Development)


# import all views
# from views import *
from views.views import *


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=config.Development.FLASK_DEBUG,port=8080)