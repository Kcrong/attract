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
    title = db.Column(db.String(30))
    details = db.Column(db.String(300))
    active_yn = db.Column(db.BOOLEAN, default=True)

    def __init__(self, title, details, party):
        self.title = title
        self.details = details
        self.party = party
