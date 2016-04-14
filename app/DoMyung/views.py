# -*-coding: utf-8 -*-
import json
import os
import random
import string

from flask import request, render_template, send_from_directory, session, redirect, url_for
from flask.ext.login import login_required, current_user
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
    p = Promise(data['title'], data['details'], data['date'])  # data['date'] = YYYYMMDD
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
    ip_addr = request.remote_addr

    req_promise = Promise.query.filter_by(title=title).first()

    user_like = req_promise.likes.filter_by(ip=ip_addr).first()

    if user_like is None:
        new_like = Like(ip_addr)

        db.session.add(new_like)
        req_promise.likes.append(new_like)

        db.session.commit()
        return redirect(url_for('.timeline'))

    else:
        return redirect(url_for('.timeline', error="이미 좋아요 버튼을 누르셨습니다."))


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
    like = db.session.query(Like).filter_by(promise=promise.id)
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
    error = request.args.get('error')

    years = [year_tuple[0]
             for year_tuple in
             Promise.query.group_by(func.year(Promise.date)).with_entities(func.year(Promise.date)).all()]

    all_promises = dict()

    for year in years:
        all_promises[str(year)] = Promise.query.filter(extract('year', Promise.date) == year).all()

    return render_template('domyung/timeline.html',
                           promise_data=all_promises,
                           years=years,
                           username=current_user,
                           error=error)


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
