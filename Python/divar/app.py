from divar import config
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import  Mail
from flask_wtf.csrf import CSRFProtect,CSRFError

app = Flask(__name__)
app.config.from_object(config.Development)
Session(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
mail = Mail(app)

from views.views import *

# all error handlers here
@app.errorhandler(CSRFError)
def csrf_error(e):
    return "درخواست دارای اشکال است"


# sender = 'alisharifihashjin@gmail.com'
# recipients = ['alisharifyofficial@gmail.com']
# subject = 'hello' 
# body = 'hello'
# mail.send_message(sender=sender,recipients= recipients,subject=subject, body=body)
# print("snd" * 100)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=config.Development.FLASK_DEBUG,port=8080)