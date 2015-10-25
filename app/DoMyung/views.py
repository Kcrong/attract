from models import Party
from models import Promise
from flask import request
from . import domyung_bp

from .. import db


@domyung_bp.route('/add', methods=['GET', 'POST'])
def add_promise():
    data = request.form
    party = db.session.query(Party).filter_by(id=data['party']).first()
    p = Promise(data['title'], data['details'], party)
    db.session.add(p)
    db.session.commit()


@domyung_bp.route('/del', methods=['GET', 'POST'])
def del_promise():
    data = request.form
    party = db.session.query(Party).filter_by(id=data['party']).first()
    p = db.session.query(Promise).filter_by(title=data['title'], details=data['details'], party=party).first()
    db.session.delete(p)
    db.session.commit()


@domyung_bp.route('/list', methods=['GET'])
def show_promise():
    return "fixing..."
