from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app)
# api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from app import routes, models

# api.add_resource(resources.UserLogin, '/api/login')
# api.add_resource(resources.UserLogoutAccess, '/api/logout/access')
# api.add_resource(resources.UserLogoutRefresh, '/api/logout/refresh')
# api.add_resource(resources.TokenRefresh, '/api/token/refresh')
# api.add_resource(resources.Farms, '/api/farms')
