from flask import request, jsonify
from flask_restful import Resource

from app.models import Group, SubGroup, SubSubGroup
from app.models import Food, Component, FoodComponent
from app.models import Source, User
from app import db
from app.api import bp
from app.api.errors import error_response, bad_request


@bp.route('/groups/<int:id>', methods=['GET'])
def get_group(id):
    return jsonify(Group.query.get_or_404(id).to_dict())


@bp.route('/sgroups/<int:id>', methods=['GET'])
def get_sgroup(id):
    return jsonify(SubGroup.query.get_or_404(id).to_dict())


@bp.route('/ssgroups/<int:id>', methods=['GET'])
def get_ssgroup(id):
    return jsonify(SubSubGroup.query.get_or_404(id).to_dict())