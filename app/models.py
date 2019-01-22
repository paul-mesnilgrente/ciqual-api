from app import db, login

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

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
    
    sub_groups = db.relationship('SubGroup', backref='group', lazy='dynamic')

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
    
    sub_sub_group = db.relationship('SubSubGroup', backref='sub_group', lazy='dynamic')

    def __eq__(self, other):
        if other == None:
            return False
        return self.id == other.id

    def __repr__(self):
        return str(self.id) + ': ' + self.name_en


class SubSubGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    name_fr = db.Column(db.String(256), index=True, unique=False)
    name_en = db.Column(db.String(256), index=True, unique=False)
    
    sub_group_id = db.Column(db.Integer, db.ForeignKey('sub_group.id'))

    foods = db.relationship('Food', backref='sub_sub_group', lazy='dynamic')

    def __eq__(self, other):
        if other == None:
            return False
        return self.id == other.id

    def __repr__(self):
        return str(self.code) + ': ' + self.name_en


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_fr = db.Column(db.String(256), index=True, unique=False)
    name_en = db.Column(db.String(256), index=True, unique=False)

    sub_sub_group_id = db.Column(db.Integer, db.ForeignKey('sub_sub_group.id'))

    food_components = db.relationship('FoodComponent', backref='food', lazy='dynamic')

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