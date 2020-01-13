import os
base_dir = os.path.abspath(os.path.dirname(__name__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "postgresql://localhost/t90farms"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or \
        "JWT-TOP-SECRET-CODE"
    FARM_BOT_USER = os.environ.get("FARM_BOT_USER") or \
        "FARM_BOT"
    FARM_BOT_PW = os.environ.get("FARM_BOT_PW") or \
        "FARM-BOTS-TOP-SECRET-CODE"
