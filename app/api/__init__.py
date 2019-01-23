from flask import Blueprint
from app import api
from flask_restful import Resource

bp = Blueprint('api', __name__)

from app.api import food, users, errors