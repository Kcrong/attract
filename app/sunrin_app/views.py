# -*-coding:utf-8-*-

from flask import render_template, redirect, url_for, send_from_directory, request, flash, session
from login_manage import User, login_manager
from .. import app
from . import sunrin_app_blueprint
from flask_login import current_user, login_user, logout_user, login_required
from db_manage import *
from flask.ext.oauth import OAuth

oauth = OAuth()

facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key='915349015224229',
                            consumer_secret='5498d66f4cf5c9a1371fd73d14016840',
                            request_token_params={'scope': 'email'}
                            )


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
    return "Hello %s" % session['username']


@sunrin_app_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated is not False:
        return redirect('/')
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form['id']
        password = request.form['password']

        if db_user_check(userid, password):
            user = User(userid)
            login_user(user)
            session['username'] = userid
            return redirect(url_for('.home'))

        else:
            return 'Bad Login'


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or '/home'

    if resp is None:
        flash('You denied the login')
        return redirect(next_url)

    session['fb_access_token'] = (resp['access_token'], '')

    me = facebook.get('/me')
    fb_id = me.data['id']
    fb_name = me.data['name']
    user = db_fb_user_check(fb_id)
    if user is None:
        db_add_fb_info(me)

    session['user_id'] = fb_id
    session['username'] = fb_name

    flash('You are now logged in as %s' % fb_name)
    return redirect(next_url)


@sunrin_app_blueprint.route('/login_fb', methods=['GET'])
def fb_login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=request.args.get('next') or request.referrer or None,
                                               _external=True))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('fb_access_token')


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
    return redirect(url_for('.index'))


@sunrin_app_blueprint.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@sunrin_app_blueprint.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)


@sunrin_app_blueprint.route('/images/<path:filename>')
def img_static(filename):
    return send_from_directory(app.root_path + '/static/images/', filename)
