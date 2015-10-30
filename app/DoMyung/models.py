# -*-coding: utf-8 -*-
from .. import db


class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    promises = db.relationship('Promise', lazy='dynamic', backref='Party')

    def __init__(self, title):
        self.title = title


class Promise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party = db.Column(db.Integer, db.ForeignKey('party.id'))
    date = db.Column(db.DATE, nullable=False)
    title = db.Column(db.String(30))
    details = db.Column(db.String(300))
    percentage = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, title, details, party, date):
        self.title = title
        self.details = details
        self.party = party
        self.date = date
