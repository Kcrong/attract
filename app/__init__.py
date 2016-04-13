import os

from flask import Flask, redirect, url_for
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

try:
    import MySQLdb
except ImportError:
    import pymysql

    pymysql.install_as_MySQLdb()

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=tmpl_dir)
db = SQLAlchemy()


def create_app():
    from .sunrin_app import sunrin_app_blueprint
    from .account import account_bp
    from .DoMyung import domyung_bp

    app.register_blueprint(sunrin_app_blueprint)
    app.register_blueprint(account_bp, url_prefix='/account')
    app.register_blueprint(domyung_bp, url_prefix='/domyung')
    app.config.from_pyfile('../config.cfg')
    return app


db.init_app(app)

from .models import *

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)

login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('account.login'))


admin = Admin(app)
admin.add_view(ModelView(Promise, db.session))
admin.add_view(ModelView(Checklist, db.session))


def trim(string):
    res = string.replace(":", "-")
    res = res.replace(".", "")
    res = res.replace("?", "q")
    return res.replace(" ", "-").replace("(", "").replace(")", "")


app.jinja_env.globals.update(clever_function=trim)
