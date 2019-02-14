from flask import request, jsonify
from flask_restful import Resource

from app.models import Group, SubGroup, SubSubGroup
from app.models import Food, Component, FoodComponent
from app.models import Source, User
from app import db
from app.api import bp
from app.api.errors import error_response, bad_request

"""
GROUPS
"""

@bp.route('/groups', methods=['GET'])
def get_groups():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Group.to_collection_dict(Group.query, page, per_page, 'api.get_groups')
    return jsonify(data)


@bp.route('/groups/<int:id>', methods=['GET'])
def get_group(id):
    return jsonify(Group.query.get_or_404(id).to_dict())


@bp.route('/groups/<int:id>/sgroups', methods=['GET'])
def get_group_sgroups(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = SubGroup.to_collection_dict(
        SubGroup.query.filter_by(group_id=id),
        page,
        per_page,
        'api.get_group_sgroups',
        id=id
    )
    return jsonify(data)

@bp.route('/groups/<int:group_id>/sgroups/<int:sgroup_id>/ssgroups', methods=['GET'])
def get_group_sgroups_ssgroups(group_id, sgroup_id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = SubGroup.to_collection_dict(
        SubSubGroup.query.filter_by(sub_group_id=sgroup_id),
        page,
        per_page,
        'api.get_group_sgroups_ssgroups',
        group_id=group_id,
        sgroup_id=sgroup_id
    )
    return jsonify(data)

"""
SUB GROUPS
"""

@bp.route('/sgroups', methods=['GET'])
def get_sgroups():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = SubGroup.to_collection_dict(SubGroup.query, page, per_page, 'api.get_sgroups')
    return jsonify(data)


@bp.route('/sgroups/<int:id>', methods=['GET'])
def get_sgroup(id):
    return jsonify(SubGroup.query.get_or_404(id).to_dict())


@bp.route('/ssgroups', methods=['GET'])
def get_ssgroups():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = SubSubGroup.to_collection_dict(SubSubGroup.query, page, per_page, 'api.get_ssgroups')
    return jsonify(data)


@bp.route('/ssgroups/<int:id>', methods=['GET'])
def get_ssgroup(id):
    return jsonify(SubSubGroup.query.get_or_404(id).to_dict())