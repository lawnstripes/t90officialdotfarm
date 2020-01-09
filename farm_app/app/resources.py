from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field is required', required=True)
parser.add_argument('password', help='This field is required', required=True)


class UserLogin(Resource):
    def post(self):
        # data = parser.parse_args()
        pass


class UserLogoutAccess(Resource):
    def post(self):
        pass


class UserLogoutRefresh(Resource):
    def post(self):
        pass


class TokenRefresh(Resource):
    def post(self):
        pass


"""
class Farms(Resource):
    def get(self):
        pass

    def put(self):
        pass
"""
