# -*-coding:utf-8-*-

from flask import render_template, redirect, url_for, send_from_directory, request
from login_manage import User, login_manager
from .. import app
from . import sunrin_app_blueprint
from flask_login import current_user, login_user, logout_user, login_required
from db_manage import *


@login_manager.user_loader
def user_loader(email):
    user = User(email)
    return user


@sunrin_app_blueprint.route('/')
def index():
    return render_template('index.html')


@sunrin_app_blueprint.route('/home')
@login_required
def home():
    return "Protected Page."


@sunrin_app_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated is not False:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form['id']
        password = request.form['password']

        if db_user_check(userid, password):
            user = User(userid)
            login_user(user)
            return redirect('/home')

        else:
            return 'Bad Login'


@sunrin_app_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def redirect_login():
    return redirect('/login')


@sunrin_app_blueprint.errorhandler(404)
def error_404(error):
    return redirect(url_for('index'))


@sunrin_app_blueprint.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@sunrin_app_blueprint.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)


@sunrin_app_blueprint.route('/images/<path:filename>')
def img_static(filename):
    return send_from_directory(app.root_path + '/static/images/', filename)
