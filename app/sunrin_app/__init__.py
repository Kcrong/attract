# -*- coding:utf-8 -*-
from flask import Blueprint
sunrin_app_blueprint = Blueprint('sunrin_app', __name__)
from . import views
