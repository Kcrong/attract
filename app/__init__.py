from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=tmpl_dir)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


def create_app():
    from sunrin_app import sunrin_app_blueprint
    app.register_blueprint(sunrin_app_blueprint)
    app.config.from_pyfile('../config.cfg')
    return app
