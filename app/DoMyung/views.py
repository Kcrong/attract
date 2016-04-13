# -*-coding: utf-8 -*-
import json
import os
import random
import string

from flask import request, render_template, send_from_directory, session, redirect, url_for
from sqlalchemy import extract
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from . import domyung_bp
from ..models import *


def randomkey(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


domyung_bp.static_folder = os.path.join(domyung_bp.root_path, '../static/')


@domyung_bp.route('/add', methods=['POST'])
def add_promise():
    data = request.form
    party = db.session.query(Party).filter_by(id=data['party']).first()
    p = Promise(data['title'], data['details'], party.id, data['date'])  # data['date'] = YYYYMMDD
    db.session.add(p)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return "Duplicate key: %s" % e.args[0].split('for key')[1].split("'")[1]
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


@domyung_bp.route('/add_like', methods=['GET'])
def add_like():
    title = request.args['title']
    try:
        username = session['username']
    except KeyError:
        return redirect(url_for('/account.fb_login'))
    promise = db.session.query(Promise).filter_by(title=title).first()

    tmp = db.session.query(Likes).filter_by(promise=promise.id, ip=username).first()
    if tmp is None:
        pass
    else:
        return "DUP!! Already Press Like Buttom."

    db.session.add(Likes(promise.id, True, username))
    db.session.commit()
    return redirect(url_for('.timeline'))


@domyung_bp.route('/select')
def select():
    return render_template('domyung/select.html')


@domyung_bp.route('/result')
def select_result():
    party = request.args['party']
    return render_template('domyung/result.html', party=party)


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


@domyung_bp.route('/add_checklist', methods=['POST'])
def add_checklist():
    data = request.form
    page = data['page']
    title = data['detail_title']
    description = data['description']
    promise = data['promise']
    image = request.files['image']
    filename = randomkey(len(image.filename)) + '.' + image.filename.rsplit('.', 1)[1]
    path = '../static/images/checklist/' + filename
    path = os.path.join(domyung_bp.root_path, path)

    image.save(path)
    promise_obj = db.session.query(Promise).filter_by(title=promise).first()
    db.session.add(Checklist(page, filename, description, title, promise_obj.id))
    db.session.commit()
    return redirect('/account/setting?promise=' + promise)


@domyung_bp.route('/timeline')
def timeline():
    try:
        username = session['username']
    except KeyError:
        username = 'Anonymous'
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
                   'promise_percent': promise.percentage,
                   'promise_likes': db.session.query(Likes).filter_by(promise=promise.id).count()}
            promises.append(tmp)

        all_promises[str(year)] = promises

    return render_template('timeline.html',
                           promise_data=all_promises,
                           years=years,
                           username=username)


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
