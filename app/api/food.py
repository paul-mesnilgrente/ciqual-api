from flask import request, jsonify
from flask_restful import Resource

from app.models import Group, SubGroup, SubSubGroup
from app.models import Food, Component, FoodComponent
from app.models import Source, User
from app import db
from app.api import bp
from app.api.errors import error_response, bad_request


@bp.route('/foods', methods=['GET'])
def get_foods():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Food.to_collection_dict(Food.query, page, per_page, 'api.get_foods')
    return jsonify(data)


@bp.route('/foods/<int:id>', methods=['GET'])
def get_food(id):
    return jsonify(Food.query.get_or_404(id).to_dict())


@bp.route('/search/food/<string:local>/<string:name>', methods=['GET'])
def search_food(local, name):
    # local = request.args.get('local', 'en', type=str)
    # name = request.args.get('name', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    if local not in ['fr', 'en']:
        return bad_request('Wrong local, fr|en')
    attrib = Food.name_en if local == 'en' else Food.name_fr

    data = Food.to_collection_dict(
        Food.query.filter(attrib.like('%{}%'.format(name))),
        page,
        per_page,
        'api.search_food',
        local=local,
        name=name
    )

    return jsonify(data)