from . import sunrin_app_blueprint
from flask_login import LoginManager, UserMixin

login_manager = LoginManager()


@sunrin_app_blueprint.record_once
def on_load(state):
    login_manager.init_app(state.app)


class User(UserMixin):
    def __init__(self, username):
        self.id = username
