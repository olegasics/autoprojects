from flask import render_template, redirect, request, url_for, flash, session, abort
from flask_login import login_user
from flask_mail import Message
from flask_classy import FlaskView, route
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User, load_user
from db_config import db, app, mail
from apps.auth.models import User, Role


class UsersView(FlaskView):
    def get(self, id):
        login = request.form['login']
        password = request.form['password']

        if login and password:
            user = User.query.filter_by(login=login).first()

            if check_password_hash(user.password, password):
                login_user(user)

                return redirect(url_for('message_api'))
            else:
                flash('Login or password is not correct. Try again')
        else:
            flash('Please enter login and password fields')

    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        position = request.form.get('position')

        if not (email or password or password2 or first_name or last_name or position):
            flash('Please, enter all fields!')

        elif password2 != password:
            flash('Passwords are not equals!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(email=email, password=hash_pwd, first_name=first_name, last_name=last_name, position=position)
            db.session.add(new_user)
            db.session.commit()
            msg = Message('Зарегистрирован новый пользователь', recipients=['omaslo@fluidbusiness.ru'])
            msg.body = f'\nЗарегистрирован новый пользователь. Login - {email},' \
                       f'\nИмя - {first_name} {last_name},' \
                       f'\nДолжность - {position}'
            mail.send(msg)
            return redirect(url_for('AuthView:get'))

    def put(self, user_id):
        pass

    def delete(self, user_id):

        pass


class AuthView(FlaskView):
    def get(self):
        if 'userLogged' in session:
            return redirect(url_for('OrdersView:get'))
        return render_template('login.html')

    def post(self):
        login = request.form['login']
        password = request.form['password']

        if login and password:
            try:
                user = User.query.filter_by(email=login).first()
            except AttributeError:
                flash('Login or password is not correct. Try again')
                return render_template('login.html')
            # user = db.find_by_name_and_password(login, password)
            #
            # if not user:
            if check_password_hash(user.password, password):
                login_user(user)
                session['userLogged'] = login
                return redirect(url_for('OrdersView:get'))
            else:
                flash('Login or password is not correct. Try again')
                return render_template('login.html')
        else:
            flash('Please enter login and password fields')
            return render_template('login.html')


class RegView(FlaskView):
    def get(self):
        if 'userLogged' in session:
            return redirect(url_for('OrdersView:get'))
        return render_template('reg.html')

