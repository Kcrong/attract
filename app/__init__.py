import os

from flask import Flask, redirect, url_for
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=tmpl_dir)
db = SQLAlchemy()


def create_app():
    from .sunrin_app import sunrin_app_blueprint
    from .account import account_bp
    from .DoMyung import domyung_bp

    app.register_blueprint(sunrin_app_blueprint)
    app.register_blueprint(account_bp, url_prefix='/account')
    app.register_blueprint(domyung_bp, url_prefix='/domyung')
    app.config.from_pyfile('../config.cfg')
    return app


db.init_app(app)

from .models import *

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)

login_manager = LoginManager()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('account.login'))


admin = Admin(app)
admin.add_view(ModelView(Promise, db.session))
admin.add_view(ModelView(Checklist, db.session))


def trim(string):
    res = string.replace(":", "-")
    res = res.replace(".", "")
    res = res.replace("?", "q")
    return res.replace(" ", "-").replace("(", "").replace(")", "")


app.jinja_env.globals.update(clever_function=trim)


def init_db():
    # add party
    p1 = Party('SinMyung')
    p2 = Party('DoDream')
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()

    sinmyung = db.session.query(Party).filter_by(id=1).first()
    dodream = db.session.query(Party).filter_by(id=2).first()

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

    return "Success"


manager.add_command('init_db', init_db)
