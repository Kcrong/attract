from models import Party
from models import Promise
from models import Likes
from flask import request, render_template, send_from_directory
import json
from . import domyung_bp
from sqlalchemy import extract
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from .. import db


@domyung_bp.route('/add', methods=['POST'])
def add_promise():
    data = request.form
    party = db.session.query(Party).filter_by(id=data['party']).first()
    p = Promise(data['title'], data['details'], party.id, data['date'])  # data['date'] = YYYYMMDD
    db.session.add(p)
    try:
        db.session.commit()
    except IntegrityError, e:
        db.session.rollback()
        return "Duplicate key: %s" % e[0].split('for key')[1].split("'")[1]
    return "Success"


@domyung_bp.route('/del', methods=['DELETE'])
def del_promise():
    data = request.args
    party = db.session.query(Party).filter_by(id=data['party']).first()
    p = db.session.query(Promise).filter_by(title=data['title'], details=data['details'], party=party.id).first()
    if p is None:
        return "There is no promise like that"
    db.session.delete(p)
    db.session.commit()
    return "Success"


@domyung_bp.route('/list', methods=['GET'])
def show_promise():
    data = []
    party_id = request.args['party']
    party = db.session.query(Party).filter_by(id=party_id).first()
    promise_list = db.session.query(Promise).filter_by(party=party.id).all()
    # party is 0 or 1
    for promise in promise_list:
        tmp = {'party': promise.party, 'title': promise.title, 'details': promise.details}
        data.append(tmp)
    return json.dumps(data)


@domyung_bp.route('/like_promise', methods=['POST'])
def like_promise():
    data = request.form
    party = db.session.query(Party).filter_by(id=data['party']).first()
    promise = db.session.query(Promise).filter_by(party=party.id, date=data['date'])
    like = db.session.query(Likes).filter_by(promise=promise.id)
    like.like = data['like']
    db.session.commit()
    return True


@domyung_bp.route('/edit_percentage', methods=['POST'])
def edit_percentage():
    data = request.form
    party = db.session.query(Party).filter_by(id=data['party']).first()
    promise = db.session.query(Promise).filter_by(party=party.id, title=data['title'], date=data['date']).first()
    promise.percentage = data['percent']
    db.session.commit()
    return "Success"


@domyung_bp.route('/timeline')
def timeline():
    date_range = db.session.query(func.min(Promise.date).label("min_year"),
                                  func.max(Promise.date).label("max_year")).one()
    years = range(date_range[0].year, date_range[1].year + 1)

    all_promises = {}

    for year in years:
        year_promises = db.session.query(Promise).filter(extract('year', Promise.date) == year).all()
        promises = []
        for promise in year_promises:
            tmp = {'promise_title': promise.title,
                   'promise_info': promise.details,
                   'promise_date': promise.date,
                   'promise_party': promise.party,
                   'promise_percent': promise.percentage}
            promises.append(tmp)

        all_promises[str(year)] = promises

    return render_template('timeline.html',
                           promise_data=all_promises,
                           years=years)


# for send static files

@domyung_bp.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(domyung_bp.root_path + '/../static/css/', filename)


@domyung_bp.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(domyung_bp.root_path + '/../static/js/', filename)


@domyung_bp.route('/img/<path:filename>')
def img_static(filename):
    return send_from_directory(domyung_bp.root_path + '/../static/images/', filename)
