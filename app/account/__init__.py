# -*- coding:utf-8 -*-
from flask import Blueprint
account_bp = Blueprint('/account', __name__)
from . import views
