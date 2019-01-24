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
    if local not in ['fr', 'en']:
        return bad_request('Wrong local, fr|en')

    sql = "SELECT * FROM food WHERE name_{} like '%{}%'".format(local, name)
    l = []
    for row in db.engine.execute(sql):
        food = Food(id=int(row[0]),
                    name_fr=row[1],
                    name_en=row[2],
                    sub_sub_group_id=int(row[3])
                )
        l.append(food.to_dict_for_collection())
    return jsonify(l)
