# -*-coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, flash, session
from flask.ext.oauth import OAuth
from flask_login import login_user, logout_user, login_required
from ..models import *

from . import account_bp
from .. import app, db

oauth = OAuth()

facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key='915346845224446',
                            consumer_secret='2afc33a5d8ade7829ece293573b10c40',
                            request_token_params={'scope': 'email'}
                            )


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


@app.route('/account/login/facebook')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or '/account/me'
    if resp is None:
        flash('You denied the login')
        return redirect(next_url)

    session['fb_access_token'] = (resp['access_token'], '')

    me = facebook.get('/me')
    data = me.data
    fb_id = data['id']
    fb_name = data['name']
    user = db.session.query(Users).filter_by(fb_id=fb_id, active_yn=True).first()

    if user is None:
        u = Users(fb_id=data['id'], name=data['name'])
        db.session.add(u)
        db.session.commit()

    session['user_id'] = fb_id
    session['username'] = fb_name

    flash('You are now logged in as %s' % fb_name)
    return redirect(next_url)


@account_bp.route('/login_fb', methods=['GET'])
def fb_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=request.args.get('next') or request.referrer or None,
                                               _external=True))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('fb_access_token')


@account_bp.route('/setting', methods=['GET'])
@login_required
def setting():
    # return "fixing..."

    promise = request.args['promise']

    # promise_db = db.session.query(Promise).filter_by(title=promise).first()
    # checklists = db.session.query(Checklist).filter_by(promise=promise_db.id).all()
    return render_template('account/admin.html',
                           promise=promise)


@account_bp.route('/add_dummy_data_db')
def dummy_db_data():
    db.session.add(Users('dodream', 'dodream123', None, u'두드림'))
    db.session.add(Users('dodream', 'dodream123', None, u'신명'))
    db.session.commit()

    return "Success"
