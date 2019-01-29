from app import db, login

from flask import url_for
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict_for_collection() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_fr = db.Column(db.String(256), index=True, unique=True)
    name_en = db.Column(db.String(256), index=True, unique=True)
    
    sgroups = db.relationship('SubGroup', back_populates='group')
    foods = db.relationship('Food', back_populates='group')

    def to_dict(self):
        return {
            '_links': {
                'self': url_for('api.get_group', id=self.id)
            },
            'id': self.id,
            'name_en': self.name_en,
            'name_fr': self.name_fr
        }

    def __eq__(self, other):
        if other == None:
            return False
        return self.id == other.id

    def __repr__(self):
        return str(self.id) + ': ' + self.name_en


class SubGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_fr = db.Column(db.String(256), index=True, unique=True)
    name_en = db.Column(db.String(256), index=True, unique=True)

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    
    group = db.relationship('Group', back_populates='sgroups')
    ssgroups = db.relationship('SubSubGroup', back_populates='sgroup')
    foods = db.relationship('Food', back_populates='sgroup')

    def to_dict(self):
        return {
            '_links': {
                'self': url_for('api.get_sgroup', id=self.id),
                'group': url_for('api.get_group', id=self.group.id)
            },
            'id': self.id,
            'name_en': self.name_en,
            'name_fr': self.name_fr
        }

    def __eq__(self, other):
        if other == None:
            return False
        return self.id == other.id

    def __repr__(self):
        return str(self.id) + ': ' + self.name_en


class SubSubGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_fr = db.Column(db.String(256), index=True, unique=False)
    name_en = db.Column(db.String(256), index=True, unique=False)
    
    sub_group_id = db.Column(db.Integer, db.ForeignKey('sub_group.id'))

    sgroup = db.relationship('SubGroup', back_populates='ssgroups')
    foods = db.relationship('Food', back_populates='ssgroup')

    def to_dict(self):
        return {
            '_links': {
                'self': url_for('api.get_ssgroup', id=self.id),
                'sgroup': url_for('api.get_sgroup', id=self.sgroup.id),
                'group': url_for('api.get_sgroup', id=self.sgroup.group.id)
            },
            'id': self.id,
            'name_en': self.name_en,
            'name_fr': self.name_fr
        }

    def __eq__(self, other):
        if other == None:
            return False
        return self.id == other.id

    def __repr__(self):
        return '{}/{}/{}: {}'.format(
            self.id,
            self.sgroup.id,
            self.sgroup.group.id,
            self.name_en
        )


class Food(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_fr = db.Column(db.String(256), index=True, unique=False)
    name_en = db.Column(db.String(256), index=True, unique=False)

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    sub_group_id = db.Column(db.Integer, db.ForeignKey('sub_group.id'))
    sub_sub_group_id = db.Column(db.Integer, db.ForeignKey('sub_sub_group.id'))

    group = db.relationship('Group', back_populates='foods')
    sgroup = db.relationship('SubGroup', back_populates='foods')
    ssgroup = db.relationship('SubSubGroup', back_populates='foods')
    food_components = db.relationship('FoodComponent', backref='food', lazy='dynamic')

    def to_dict_for_collection(self):
        return {
            '_links': {
                'details': url_for('api.get_food', id=self.id),
                'group': url_for('api.get_group', id=self.group.id),
                'sub_group': url_for('api.get_sgroup', id=self.sgroup.id),
                'sub_sub_group': url_for('api.get_ssgroup', id=self.ssgroup.id)
            },
            'id': self.id,
            'name_fr': self.name_fr,
            'name_en': self.name_en,
            # 'components': {
            #     'Energie': {
            #         'min': None,
            #         'max': 35.0,
            #         'quantity': '-'
            #     }
            # }
        }

    def to_dict(self):
        components = [fc.to_dict() for fc in self.food_components]
        return {
            '_links': {
                'self': url_for('api.get_food', id=self.id),
                'group': url_for('api.get_group', id=self.group.id),
                'sub_group': url_for('api.get_sgroup', id=self.sgroup.id),
                'sub_sub_group': url_for('api.get_ssgroup', id=self.ssgroup.id)
            },
            'id': self.id,
            'name_fr': self.name_fr,
            'name_en': self.name_en,
            # 'components': {
            #     'Energie': {
            #         'min': None,
            #         'max': 35.0,
            #         'quantity': '-'
            #     }
            # }
            'components': components
        }

    def __repr__(self):
        return str(self.id) + ': ' + self.name_en


class FoodComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    min = db.Column(db.Float)
    max = db.Column(db.Float)
    quantity = db.Column(db.String(5))
    trust_code = db.Column(db.CHAR)

    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    component_id = db.Column(db.Integer, db.ForeignKey('component.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))

    component = db.relationship('Component', foreign_keys=component_id)
    source = db.relationship('Source', foreign_keys=source_id)

    def to_dict(self):
        return {
            'name_fr': self.component.name_fr,
            'name_en': self.component.name_en,
            'min': self.min,
            'max': self.max,
            'quantity': self.quantity,
            'trust_code': self.trust_code
        }

    def __repr__(self):
        return 'Component(food_id={}, component_id={}, source_id={}, ' + \
            'min={}, max={}, quantity={}, trust_code={})'.format(
                self.food_id, 
                self.component_id, 
                self.source_id, 
                self.min, 
                self.max, 
                self.quantity, 
                self.trust_code
        )


class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_fr = db.Column(db.String(256), index=True, unique=True)
    name_en = db.Column(db.String(256), index=True, unique=True)

    def __repr__(self):
        return str(self.id) + ': ' + self.name_en


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    ref_citation = db.Column(db.String(256), index=True, unique=False)

    def __repr__(self):
        if self.ref_citation:
            return str(self.code) + ': ' + self.ref_citation
        else:
            return str(self.code) + ': ' + '""'