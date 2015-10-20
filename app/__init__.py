from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=tmpl_dir)
db = SQLAlchemy()


def create_app():
    from sunrin_app import sunrin_app_blueprint
    from account import account_bp

    app.register_blueprint(sunrin_app_blueprint)
    app.register_blueprint(account_bp, url_prefix='/account')
    app.config.from_pyfile('../config.cfg')
    return app

app = create_app()
db = SQLAlchemy(app)
print dir(db)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
