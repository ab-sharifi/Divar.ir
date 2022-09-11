class config:
    SECRET_KET="temp temp temp"
    TEMPLATES_AUTO_RELOAD=True
    SESSION_PERMANENT=False
    SESSION_TYPE="filesystem"


class Development(config):
    FLASK_DEBUG=True


class Production(config):
    FLASK_DEBUG=True