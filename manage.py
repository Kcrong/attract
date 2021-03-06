# -*-coding: utf-8 -*-

from app import manager, create_app
from app.models import *

app = create_app()


@manager.command
def run():
    app.run()


@manager.command
def init_db():
    # add party
    p1 = Party('SinMyung')
    p2 = Party('DoDream')
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()

    sinmyung = db.session.query(Party).filter_by(name='SinMyung').first()
    dodream = db.session.query(Party).filter_by(name='DoDream').first()

    # add sinmyung promise
    promise = Promise('빌:공약', '여러분이 원하는 공약을 들어드립니다.', 20151010)
    promise.likes.append(Like('2.0.0.1'))
    sinmyung.promises.append(promise)
    db.session.add(promise)

    promise = Promise('선린뉴스', '한달에 한번 선린뉴스로 소식을 전하겠습니다.', 20151010)
    promise.likes.append(Like('2.0.0.2'))
    sinmyung.promises.append(promise)
    db.session.add(promise)

    promise = Promise('급식의 지니', '여러분이 먹고싶은 급식을 먹을 수 있도록 투표를 진행', 20151010)
    promise.likes.append(Like('2.0.0.3'))
    sinmyung.promises.append(promise)
    db.session.add(promise)

    promise = Promise('모두의 축제', '복면가왕등 새로워진 축제개선', 20151010)
    promise.likes.append(Like('2.0.0.4'))
    sinmyung.promises.append(promise)
    db.session.add(promise)

    promise = Promise('선림픽', '장애물 달리기, 여자종목 추가 등 새로워진 체육대회', 20151010)
    promise.likes.append(Like('2.0.0.5'))
    sinmyung.promises.append(promise)
    db.session.add(promise)

    promise = Promise('선린챔스', '리그방식으로 진행되는 선린풋살대회', 20151010)
    promise.likes.append(Like('2.0.0.6'))
    sinmyung.promises.append(promise)
    db.session.add(promise)

    promise = Promise('E-Sports', '매년 진행해온 이스포츠', 20151010)
    promise.likes.append(Like('2.0.0.7'))
    sinmyung.promises.append(promise)
    db.session.add(promise)

    promise = Promise('대여해도 대여?', '공,석식,우산,충전기를 대여해드립니다.', 20151010)
    promise.likes.append(Like('2.0.0.8'))
    sinmyung.promises.append(promise)
    db.session.add(promise)

    promise = Promise('학생증리뉴얼', '학생증 공모전을 통해 새롭게 바뀔 학생증', 20151010)
    promise.likes.append(Like('2.0.0.9'))
    sinmyung.promises.append(promise)
    db.session.add(promise)

    promise = Promise('프린터를 부탁해', '고장나서 느리고 불편했던 프린터기를 추가/교체', 20151010)
    promise.likes.append(Like('2.0.1.1'))
    sinmyung.promises.append(promise)
    db.session.add(promise)

    promise = Promise('허니버터고3', '학업에 지친 고3 선배들을 위한 작은 이벤트', 20151010)
    promise.likes.append(Like('2.0.2.1'))
    sinmyung.promises.append(promise)
    db.session.add(promise)
    db.session.commit()

    # add dodream promise
    promise = Promise('선.디.전', '선린인터넷고와 디미고의 각종 대결을 추진', 20141010)
    promise.likes.append(Like('0.0.0.1'))
    dodream.promises.append(promise)
    db.session.add(promise)

    promise = Promise('애플데이', '사과하고 싶었던 사람에게 편지를 쓰면 사과와 함께 대신 전달', 20141010)
    promise.likes.append(Like('0.0.0.2'))
    dodream.promises.append(promise)
    db.session.add(promise)

    promise = Promise('별빛이 내린다', '야자가 끝난 밤, 어두웠던 1호관 뒤쪽에 조명을 설치', 20141010)
    promise.likes.append(Like('0.0.0.3'))
    dodream.promises.append(promise)
    db.session.add(promise)

    promise = Promise('2 dream', '폰충,우산,석식,에코백,축구공,농구공 대여 및 벼룩시장', 20141010)
    promise.likes.append(Like('0.0.0.4'))
    dodream.promises.append(promise)
    db.session.add(promise)

    promise = Promise('게임채널 e', 'E-sports 게임대회를 개최', 20141010)
    promise.likes.append(Like('0.0.0.5'))
    dodream.promises.append(promise)
    db.session.add(promise)

    promise = Promise('홍보가 기가막혀', '중학교에 직접 홍보를 갈 수 있는 기회를 제공', 20141010)
    promise.likes.append(Like('0.0.0.6'))
    dodream.promises.append(promise)
    db.session.add(promise)

    promise = Promise('guess (계단스티커)', '위험했던 갈색계단에 스티커 부착, 보다 안전하게 ', 20141010)
    promise.likes.append(Like('0.0.0.7'))
    dodream.promises.append(promise)
    db.session.add(promise)

    promise = Promise('고삼 Pictures', '졸업사진을 모아 가장 재미있는 사진에 상품 증정', 20141010)
    promise.likes.append(Like('0.0.0.8'))
    dodream.promises.append(promise)
    db.session.add(promise)

    promise = Promise('구기대회', '2학기에 소규모 구기대회를 개최', 20141010)
    promise.likes.append(Like('0.0.0.9'))
    dodream.promises.append(promise)
    db.session.add(promise)

    promise = Promise('선린App 개발', '선린 앱 개발 프로젝트를 추진', 20141010)
    promise.likes.append(Like('0.0.1.0'))
    dodream.promises.append(promise)
    db.session.add(promise)

    promise = Promise('?', '건의를 받아 공약 추진', 20141010)
    promise.likes.append(Like('0.0.1.1'))
    dodream.promises.append(promise)
    db.session.add(promise)
    db.session.commit()

    db.session.add(User('dodream', 'dodream123', '두드림'))
    db.session.add(User('sinmyung', 'sinmyung123', '신명'))
    db.session.commit()
    return "Success"


if __name__ == '__main__':
    manager.run()
