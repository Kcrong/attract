from .. import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True)
    userid = db.Column(db.String(30), nullable=False, unique=False)
    password = db.Column(db.String(50), nullable=False)
    active_yn = db.Column(db.BOOLEAN(), nullable=False, default=True)

    def __init__(self, userid=None, password=None):
        self.password = password
        self.userid = userid
