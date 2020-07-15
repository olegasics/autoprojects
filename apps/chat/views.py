from flask.views import MethodView
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from apps.chat.models import Room, Message
from apps.auth.models import User
from db_config import db


class MessageAPIView(MethodView):
    @login_required
    def get(self, message_text):

        if message_text is None:
            # login = request.form['login']
            # if 'userLogged' not in session or session['userLogged'] != login:
            #     abort(401)
            rooms = Room.query.all()
            messages = Message.query.all()
            return render_template('messages.html', messages=messages, rooms=rooms)
        return '1'

    def post(self):
        text = request.form['text']
        room_id = request.form['room_id']

        room = Room.query.get(room_id)
        message = Message(text=text, room_id=room.id, user_id=1)
        db.session.add(message)
        db.session.commit()

        return redirect(url_for('room_api') + room_id)
        # return render_template('room.html', messages=messages, room=room)

    def put(self, message_id):
        pass

    def delete(self, message_id):
        pass


class RoomAPIView(MethodView):
    def get(self, room_id):
        if room_id is None:
            pass
        else:
            messages = Message.query.filter_by(room_id=room_id)
            room = Room.query.get(room_id)
            return render_template('room.html', room=room, messages=messages)

    def post(self):
        name = request.form['name']
        password = request.form['password']
        room = Room(name=name, password=password)
        db.session.add(room)
        db.session.commit()
        room = Room.query.filter_by(name=name).first()
        return render_template('room.html', room=room)

    def put(self, room_id):
        pass

    def delete(self, room_id):
        pass


class MainAPIView(MethodView):

    def get(self):
        return render_template('main.html')

    def post(self):
        pass

    def put(self, message_id):
        pass

    def delete(self, message_id):
        pass
