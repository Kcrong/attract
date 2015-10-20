# -*-coding:utf-8-*-

from . import sunrin_app_blueprint
from flask import render_template

@sunrin_app_blueprint.route('/')
def index():
    return render_template('index.html')
