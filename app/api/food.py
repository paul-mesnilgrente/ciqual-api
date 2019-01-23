from flask_restful import Resource
from app import api

class Food(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(Food, '/food')