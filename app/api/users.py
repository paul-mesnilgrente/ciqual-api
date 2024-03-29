from flask import Blueprint
from flask_restful import Resource
from app import api

from app.api import bp

class UserApi(Resource):
    def get(self):
        return {'Hello': 'You'}

api.add_resource(UserApi, '/users')