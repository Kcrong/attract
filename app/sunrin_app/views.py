# -*-coding:utf-8-*-

from . import sunrin_app_blueprint
from flask import render_template, send_from_directory, send_file, redirect


@sunrin_app_blueprint.route('/')
@sunrin_app_blueprint.route('/index')
def index():
    return render_template('index.html')


@sunrin_app_blueprint.route('/select')
def go_select():
    return render_template('select.html')


@sunrin_app_blueprint.route('/timeline')
def go_timeline():
    return redirect('/domyung/timeline')


@sunrin_app_blueprint.route('/admin')
def promise_list():
    return render_template('promise_list.html')


@sunrin_app_blueprint.route('/testing')
def complete_select():
    return render_template('complete_select.html')

# for send static files

@sunrin_app_blueprint.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(sunrin_app_blueprint.root_path + '/../static/css/', filename)


@sunrin_app_blueprint.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(sunrin_app_blueprint.root_path + '/../static/js/', filename)


@sunrin_app_blueprint.route('/img/<path:filename>')
def img_static(filename):
    return send_from_directory(sunrin_app_blueprint.root_path + '/../static/images/', filename)


@sunrin_app_blueprint.route('/favicon.ico')
def favicon():
    return send_file(sunrin_app_blueprint.root_path + '/../static/images/favicon.ico')
