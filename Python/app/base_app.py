# base flask app located in here
# via import from this package we can user app variable

from flask import Flask
from flask_session import Session

app = Flask(__name__)
Session(app)

