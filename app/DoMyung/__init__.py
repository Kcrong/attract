# -*- coding:utf-8 -*-
from flask import Blueprint
domyung_bp = Blueprint('/domyung', __name__)
from . import views
