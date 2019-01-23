from flask import request, jsonify
from flask_restful import Resource

from app.models import Group, SubGroup, SubSubGroup
from app.models import Food, Component, FoodComponent
from app.models import Source, User
from app.api import bp


@bp.route('/foods', methods=['GET'])
def get_foods():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Food.to_collection_dict(Food.query, page, per_page, 'api.get_foods')
    return jsonify(data)


@bp.route('/foods/<int:id>', methods=['GET'])
def get_food(id):
    return jsonify(Food.query.get_or_404(id).to_dict())