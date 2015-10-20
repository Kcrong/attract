from .. import db


class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),unique=True)
    promises = db.relationship('Promise', lazy='dynamic', backref='party')


class Promise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party = db.Column(db.Integer, db.ForeignKey('party.id'))
    title = db.Column(db.String(30), unique=True)
    details = db.Column(db.String(300))

    def __init__(self, title, details, party):
        self.title = title
        self.details = details
        self.party = party
