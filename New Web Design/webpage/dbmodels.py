from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    iconFile = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    user_groups = db.relationship('UserGroup', backref='user', lazy=True)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    user_groups = db.relationship('UserGroup', backref='group', lazy=True)

class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_manager = db.Column(db.Boolean)

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    iconFile = db.Column(db.String(150))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_groups = db.relationship('CompetitionGroup', backref='group', lazy=True)

class CompetitionGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    
    