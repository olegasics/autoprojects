from datetime import datetime

from db_config import db

user_room = db.Table('user_room',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('room_id', db.Integer, db.ForeignKey('room.id'), primary_key=True))


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(500), nullable=True)
    users = db.relationship('User', secondary=user_room, lazy='subquery',
                            backref=db.backref('rooms', lazy=True))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
