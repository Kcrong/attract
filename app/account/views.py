# -*-coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, session
from flask_login import login_user, logout_user, login_required

from . import account_bp
from ..models import *


@account_bp.route('/me')
@login_required
def home():
    return "Hello %s" % session['username']


@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        username = session['username']
    except KeyError:
        pass
    else:
        if username == 'dodream' or username == 'sinmyung':
            redirect(url_for('/domyung.timeline'))
    if request.method == 'GET':
        return render_template('account/login.html')
    else:
        userid = request.form['id']
        password = request.form['password']
        u = db.session.query(Users).filter_by(userid=userid, password=password, active_yn=True).first()
        if u is not None:
            user = User(userid)
            login_user(user)
            session['username'] = userid
            return redirect(url_for('admin.index'))
        else:
            return 'Bad Login'


@account_bp.route('/logout')
@login_required
def logout():
    logout_user()
    del session['username']
    return redirect(url_for('domyung.timeline'))


@account_bp.route('/setting', methods=['GET'])
@login_required
def setting():
    promise = request.args['promise']

    return render_template('account/admin.html',
                           promise=promise)


@account_bp.route('/add_dummy_data_db')
def dummy_db_data():
    return "Success"
