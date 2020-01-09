from flask import Flask
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
api = Api(app)


from app import routes, resources, models


api.add_resource(resources.UserLogin, '/api/login')
api.add_resource(resources.UserLogoutAccess, '/api/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/api/logout/refresh')
api.add_resource(resources.TokenRefresh, '/api/token/refresh')
# api.add_resource(resources.Farms, '/api/farms')
