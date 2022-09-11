# this is a pseudo base flask app  
# but the actually flask app located in app module(base_app.py)

import flask
import config 
from app.base_app import app


# web app config loaded
app.config.from_object(config.Development)



# import all views
from views.views import *



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=config.Development.FLASK_DEBUG,port=8080)