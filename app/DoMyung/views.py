# -*-coding: utf-8 -*-
from models import Party
from models import Promise
from models import Likes
from models import Checklist
from flask import request, render_template, send_from_directory, session, redirect
import json
from . import domyung_bp
from sqlalchemy import extract
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from .. import db
import os
import random
import string


def randomkey(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


domyung_bp.static_folder = os.path.join(domyung_bp.root_path, '../static/')


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


@domyung_bp.route('/select')
def select():
    return render_template('select.html')


@domyung_bp.route('/result')
def select_result():
    return render_template('complete_select.html')


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


@domyung_bp.route('/add_dummy_data_db')
def dummy_db_data():
    """
    # add party
    p1 = Party('SinMyung')
    p2 = Party('DoDream')
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
    """

    sinmyung = db.session.query(Party).filter_by(id=1).first()
    dodream = db.session.query(Party).filter_by(id=2).first()

    """
    # add sinmyung promise
    promise = Promise('빌:공약', '여러분이 원하는 공약을 들어드립니다.', sinmyung.id, 20151010)
    db.session.add(promise)
    promise = Promise('선린뉴스', '한달에 한번 선린뉴스로 소식을 전하겠습니다.', sinmyung.id, 20151010)
    db.session.add(promise)
    promise = Promise('급식의 지니', '여러분이 먹고싶은 급식을 먹을 수 있도록 투표를 진행', sinmyung.id, 20151010)
    db.session.add(promise)
    promise = Promise('모두의 축제', '복면가왕등 새로워진 축제개선', sinmyung.id, 20151010)
    db.session.add(promise)
    promise = Promise('선림픽', '장애물 달리기, 여자종목 추가 등 새로워진 체육대회', sinmyung.id, 20151010)
    db.session.add(promise)
    promise = Promise('선린챔스', '리그방식으로 진행되는 선린풋살대회', sinmyung.id, 20151010)
    db.session.add(promise)
    promise = Promise('E-Sports', '매년 진행해온 이스포츠', sinmyung.id, 20151010)
    db.session.add(promise)
    promise = Promise('대여해도 대여?', '공,석식,우산,충전기를 대여해드립니다.', sinmyung.id, 20151010)
    db.session.add(promise)
    promise = Promise('학생증리뉴얼', '학생증 공모전을 통해 새롭게 바뀔 학생증', sinmyung.id, 20151010)
    db.session.add(promise)
    promise = Promise('프린터를 부탁해', '고장나서 느리고 불편했던 프린터기를 추가/교체', sinmyung.id, 20151010)
    db.session.add(promise)
    promise = Promise('허니버터고3', '학업에 지친 고3 선배들을 위한 작은 이벤트', sinmyung.id, 20151010)
    db.session.add(promise)
    db.session.commit()
    """

    """
    # add dodream promise
    promise = Promise('선.디.전', '선린인터넷고와 디미고의 각종 대결을 추진', dodream.id, 20141010)
    db.session.add(promise)
    promise = Promise('애플데이', '사과하고 싶었던 사람에게 편지를 쓰면 사과와 함께 대신 전달', dodream.id, 20141010)
    db.session.add(promise)
    promise = Promise('별빛이 내린다', '야자가 끝난 밤, 어두웠던 1호관 뒤쪽에 조명을 설치', dodream.id, 20141010)
    db.session.add(promise)
    promise = Promise('2 dream', '폰충,우산,석식,에코백,축구공,농구공 대여 및 벼룩시장', dodream.id, 20141010)
    db.session.add(promise)
    promise = Promise('게임채널 e', 'E-sports 게임대회를 개최', dodream.id, 20141010)
    db.session.add(promise)
    promise = Promise('홍보가 기가막혀', '중학교에 직접 홍보를 갈 수 있는 기회를 제공', dodream.id, 20141010)
    db.session.add(promise)
    promise = Promise('guess (계단스티커)', '위험했던 갈색계단에 스티커 부착, 보다 안전하게 ', dodream.id, 20141010)
    db.session.add(promise)
    promise = Promise('고삼 Pictures', '졸업사진을 모아 가장 재미있는 사진에 상품 증정', dodream.id, 20141010)
    db.session.add(promise)
    promise = Promise('구기대회', '2학기에 소규모 구기대회를 개최', dodream.id, 20141010)
    db.session.add(promise)
    promise = Promise('선린App 개발', '선린 앱 개발 프로젝트를 추진', dodream.id, 20141010)
    db.session.add(promise)
    promise = Promise('?', '건의를 받아 공약 추진', dodream.id, 20141010)
    db.session.add(promise)
    db.session.commit()
    """

    """
    # add promise like data
    like = Likes(1, True, '0.0.0.1')
    db.session.add(like)
    like = Likes(2, True, '0.0.0.2')
    db.session.add(like)
    like = Likes(3, True, '0.0.0.3')
    db.session.add(like)
    like = Likes(4, True, '0.0.0.4')
    db.session.add(like)
    like = Likes(5, True, '0.0.0.5')
    db.session.add(like)
    like = Likes(6, True, '0.0.0.6')
    db.session.add(like)
    like = Likes(7, True, '0.0.0.7')
    db.session.add(like)
    like = Likes(8, True, '0.0.0.8')
    db.session.add(like)
    like = Likes(9, True, '0.0.0.9')
    db.session.add(like)
    like = Likes(10, True, '0.0.1.1')
    db.session.add(like)
    like = Likes(11, True, '0.0.2.1')
    db.session.add(like)
    like = Likes(12, True, '0.0.3.1')
    db.session.add(like)
    like = Likes(13, True, '0.0.4.1')
    db.session.add(like)
    like = Likes(14, True, '0.0.5.1')
    db.session.add(like)
    like = Likes(15, True, '0.0.6.1')
    db.session.add(like)
    like = Likes(16, True, '0.0.7.1')
    db.session.add(like)
    like = Likes(17, True, '0.0.8.1')
    db.session.add(like)
    like = Likes(18, True, '0.0.9.1')
    db.session.add(like)
    like = Likes(19, True, '0.1.0.1')
    db.session.add(like)
    like = Likes(20, True, '0.2.0.1')
    db.session.add(like)
    like = Likes(21, True, '0.3.0.1')
    db.session.add(like)
    like = Likes(22, True, '0.4.0.1')
    db.session.add(like)
    db.session.commit()
    """
    return "Success"


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


"""
#@domyung_bp.route('/add_db_info')
def asdf():
    sinmyung = db.session.query(Party).filter_by(id=1).first()
    dodream = db.session.query(Party).filter_by(id=2).first()

    db.session.add(Promise('빌:공약', '여러분이 원하는 공약을 들어드립니다.', sinmyung.id, '20150101'))
    db.session.add(Promise('선린뉴스', '한달에 한 번 선린뉴스로 소식을 전하겠습니다.', sinmyung.id, '20150201'))
    db.session.add(Promise('급식의지니', '여러분이 먹고싶은 급식을 먹을 수 있도록 투표를 진행', sinmyung.id, '20150301'))
    db.session.add(Promise('모두의축제', '복면가왕 등 새로워진 축제개선', sinmyung.id, '20150401'))
    db.session.add(Promise('선림픽', '장애물 달리기, 여자종목 추가 등 새로워진 체육대회', sinmyung.id, '20150501'))
    db.session.add(Promise('선린챔스', '리그방식으로 진행되는 선린풋살대회', sinmyung.id, '20150601'))
    db.session.add(Promise('E-Sports', '매년 진행해온 E-Sports', sinmyung.id, '20150701'))
    db.session.add(Promise('대여해도 돼여?', '공, 석식, 우산, 충전기를 대여해드립니다.', sinmyung.id, '20150801'))
    db.session.add(Promise('학생증 리뉴얼', '학생증 공모전을 통해 새롭게 바뀔 학생증!', sinmyung.id, '20150901'))
    db.session.add(Promise('프린터를 부탁해', '고장나서 느리고 불편했던 프린터기를 추가/삭제', sinmyung.id, '20151001'))
    db.session.add(Promise('허니버터고3', '학업에 지친 선배들을 위한 작은 이벤트', sinmyung.id, '20151101'))

    db.session.commit()
    return "AsdF"
"""
