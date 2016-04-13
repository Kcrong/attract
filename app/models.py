from . import db
from flask.ext.login import UserMixin, AnonymousUserMixin


class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    promises = db.relationship('Promise', lazy='dynamic', backref='party')

    def __repr__(self):
        return "<Party %s>" % self.name

    def __init__(self, name):
        self.name = name


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    promise_id = db.Column(db.Integer, db.ForeignKey('promise.id'))
    active = db.Column(db.BOOLEAN, default=True)
    ip = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return "<Like %s>" % self.promise.title

    def __init__(self, ip):
        self.ip = ip


class Promise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'))
    date = db.Column(db.DATE, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(300))
    percentage = db.Column(db.Integer, nullable=False, default=0)
    likes = db.relationship(Like, lazy='dynamic', backref='promise')

    def __repr__(self):
        return "<Promise %s>" % self.title

    def __init__(self, title, detail, date):
        self.title = title
        self.detail = detail
        self.date = date


class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    promise = db.Column(db.Integer, db.ForeignKey('promise.id'))
    page = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(200))
    info = db.Column(db.String(300))
    title = db.Column(db.String(300))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    userid = db.Column(db.String(30), unique=False)
    name = db.Column(db.String(10))
    password = db.Column(db.String(50))
    active = db.Column(db.BOOLEAN, nullable=False, default=True)

    def __init__(self, userid, password, name):
        self.userid = userid
        self.password = password
        self.name = name


class GuestUser(AnonymousUserMixin):
    name = 'Guest'
