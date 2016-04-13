# -*-coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, session
from flask.ext.login import login_user, logout_user, login_required

from . import account_bp
from ..models import *


@account_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('account/login.html')
    else:
        userid = request.form['id']
        password = request.form['password']
        u = db.session.query(User).filter_by(userid=userid, password=password, active=True).first()
        if u is not None:
            login_user(u)
            return redirect(url_for('admin.index'))
        else:
            return redirect(url_for('.login'))


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
