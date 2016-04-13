from . import db
from flask.ext.login import UserMixin


class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    promises = db.relationship('Promise', lazy='dynamic', backref='Party')

    def __init__(self, title):
        self.title = title

    def __unicode__(self):
        return self.title


class Promise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party = db.Column(db.Integer, db.ForeignKey('party.id'))
    date = db.Column(db.DATE, nullable=False)
    title = db.Column(db.String(30))
    details = db.Column(db.String(300))
    percentage = db.Column(db.Integer, nullable=False, default=0)
    likes = db.relationship('Likes', lazy='dynamic', backref='Promise')

    def __init__(self, title, details, party, date):
        self.title = title
        self.details = details
        self.party = party
        self.date = date


class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    promise = db.Column(db.Integer, db.ForeignKey('promise.id'))
    like = db.Column(db.BOOLEAN)
    ip = db.Column(db.String(16))

    def __init__(self, promise, like, ip):
        self.promise = promise
        self.like = like
        self.ip = ip

    def __unicode__(self):
        res = len(list(self.query.filter_by(id=self.id)))
        return str(res)


class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    promise = db.Column(db.Integer, db.ForeignKey('promise.id'))
    page = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(200))
    info = db.Column(db.String(300))
    title = db.Column(db.String(300))

    def __init__(self, page, picture, info, title, promise):
        self.page = page
        self.picture = picture
        self.info = info
        self.title = title
        self.promise = promise


class Users(db.Model, UserMixin):
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
