# -*-coding:utf-8-*-

from flask import render_template, redirect, url_for, send_from_directory, request
from login_manage import app, User, login_manager
from database.db_manage import *
from flask_login import current_user, login_user, logout_user, login_required


@login_manager.user_loader
def user_loader(email):
    user = User(email)
    return user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('home'))

        else:
            return 'Bad Login'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'


@app.errorhandler(404)
def error_404(error):
    return redirect(url_for('index'))


@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)


@app.route('/images/<path:filename>')
def img_static(filename):
    return send_from_directory(app.root_path + '/static/images/', filename)
