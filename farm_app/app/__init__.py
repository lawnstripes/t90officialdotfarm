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
socketio = SocketIO(app)
cli = FlaskGroup(app)
application = app

from app import routes, models
