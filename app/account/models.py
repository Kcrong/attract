from .. import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True)
    userid = db.Column(db.String(30), unique=False)
    fb_id = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(10))
    password = db.Column(db.String(50))
    active_yn = db.Column(db.BOOLEAN, nullable=False, default=True)

    def __init__(self, userid=None, password=None, fb_id=None, name=None):
        self.password = password
        self.userid = userid
        self.fb_id = fb_id
        self.name = name

