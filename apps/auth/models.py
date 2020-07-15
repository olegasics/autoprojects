from flask import url_for, redirect
from sqlalchemy_serializer import SerializerMixin
from flask_login import LoginManager, UserMixin, login_required

from db_config import db
login_manager = LoginManager(db.app)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin, SerializerMixin):
    serialize_only = {
        'id',
        'email',
        'position'
    }
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(30), unique=True, nullable=False)
    last_name = db.Column(db.String(30), unique=True, nullable=False)
    active = db.Column(db.Boolean())
    position = db.Column(db.String(55))
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), unique=True)
    description = db.Column(db.String(255))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('AuthView:get'))