from config import app
from flask_login import LoginManager, UserMixin

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, username):
        self.id = username



