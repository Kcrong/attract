# -*-coding: utf-8 -*-
import os
import random
import string

from flask import request, render_template, send_from_directory, redirect, url_for
from flask.ext.login import current_user
from sqlalchemy import extract
from sqlalchemy.sql import func

from . import domyung_bp
from ..models import *


def randomkey(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


domyung_bp.static_folder = os.path.join(domyung_bp.root_path, '../static/')


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
