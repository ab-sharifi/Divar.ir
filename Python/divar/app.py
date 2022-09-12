from divar import config
from flask import Flask
from flask_session import Session

app = Flask(__name__)
app.config.from_object(config.Development)
Session(app)

from views.views import *

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=config.Development.FLASK_DEBUG,port=8080)