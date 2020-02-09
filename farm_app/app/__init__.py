from flask import Flask
from flask.cli import FlaskGroup
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO


app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
if app.config['ENV'] != 'production':
    socketio = SocketIO(app, engineio_logger=app.debug)
else:
    socketio = SocketIO(app,
                        engineio_logger=app.debug,
                        cors_allowed_origins=app.config['ALLOWED_ORIGINS'])
cli = FlaskGroup(app)
application = app

from app import routes, models
