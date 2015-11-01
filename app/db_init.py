def init_db(db, Party, Promise, Likes, Checklist):
    db.session.add(Party('DoDream'))
    db.session.add(Party('SinMyung'))
    db.session.commit()

    party = db.session.query(Party).filter_by(id=1).first()
    party2 = db.session.query(Party).filter_by(id=2).first()

    db.session.add(Promise('test_promise1', 'test_promise1_detail', party.id, '20121010'))
    db.session.add(Promise('test_promise2', 'test_promise2_detail', party2.id, '20131010'))
    db.session.add(Promise('test_promise3', 'test_promise3_detail', party.id, '20141010'))
    db.session.add(Promise('test_promise4', 'test_promise4_detail', party2.id, '20151010'))

    db.session.commit()

    promise1 = db.session.query(Promise).filter_by(title='test_promise1').first()
    promise2 = db.session.query(Promise).filter_by(title='test_promise2').first()
    promise3 = db.session.query(Promise).filter_by(title='test_promise3').first()
    promise4 = db.session.query(Promise).filter_by(title='test_promise4').first()

    db.session.add(Likes(promise1.id, True, '123.123.123.123'))
    db.session.add(Likes(promise1.id, False, '223.123.123.123'))
    db.session.add(Likes(promise1.id, True, '323.123.123.123'))
    db.session.add(Likes(promise1.id, False, '123.123.123.124'))

    db.session.add(Likes(promise2.id, True, '123.123.123.123'))
    db.session.add(Likes(promise2.id, False, '223.123.123.123'))
    db.session.add(Likes(promise2.id, True, '323.123.123.123'))
    db.session.add(Likes(promise2.id, False, '123.123.123.124'))

    db.session.add(Likes(promise3.id, True, '123.123.123.123'))
    db.session.add(Likes(promise3.id, False, '223.123.123.123'))
    db.session.add(Likes(promise3.id, True, '323.123.123.123'))
    db.session.add(Likes(promise3.id, False, '123.123.123.124'))

    db.session.add(Likes(promise4.id, True, '123.123.123.123'))
    db.session.add(Likes(promise4.id, False, '223.123.123.123'))
    db.session.add(Likes(promise4.id, True, '323.123.123.123'))
    db.session.add(Likes(promise4.id, False, '123.123.123.124'))

    db.session.commit()

    db.session.add(Checklist(1, '/img/timeline/checklist/test1.png', 'test_info', 'test_title', promise1.id))
    db.session.add(Checklist(2, '/img/timeline/checklist/test2.png', 'test_info', 'test_title', promise1.id))
    db.session.add(Checklist(3, '/img/timeline/checklist/test3.png', 'test_info', 'test_title', promise1.id))
    db.session.add(Checklist(4, '/img/timeline/checklist/test4.png', 'test_info', 'test_title', promise1.id))
    db.session.add(Checklist(5, '/img/timeline/checklist/test5.png', 'test_info', 'test_title', promise1.id))

    db.session.add(Checklist(1, '/img/timeline/checklist/test1.png', 'test_info', 'test_title', promise2.id))
    db.session.add(Checklist(2, '/img/timeline/checklist/test2.png', 'test_info', 'test_title', promise2.id))
    db.session.add(Checklist(3, '/img/timeline/checklist/test3.png', 'test_info', 'test_title', promise2.id))
    db.session.add(Checklist(4, '/img/timeline/checklist/test4.png', 'test_info', 'test_title', promise2.id))
    db.session.add(Checklist(5, '/img/timeline/checklist/test5.png', 'test_info', 'test_title', promise2.id))

    db.session.add(Checklist(1, '/img/timeline/checklist/test1.png', 'test_info', 'test_title', promise3.id))
    db.session.add(Checklist(2, '/img/timeline/checklist/test2.png', 'test_info', 'test_title', promise3.id))
    db.session.add(Checklist(3, '/img/timeline/checklist/test3.png', 'test_info', 'test_title', promise3.id))
    db.session.add(Checklist(4, '/img/timeline/checklist/test4.png', 'test_info', 'test_title', promise3.id))
    db.session.add(Checklist(5, '/img/timeline/checklist/test5.png', 'test_info', 'test_title', promise3.id))

    db.session.add(Checklist(1, '/img/timeline/checklist/test1.png', 'test_info', 'test_title', promise4.id))
    db.session.add(Checklist(2, '/img/timeline/checklist/test2.png', 'test_info', 'test_title', promise4.id))
    db.session.add(Checklist(3, '/img/timeline/checklist/test3.png', 'test_info', 'test_title', promise4.id))
    db.session.add(Checklist(4, '/img/timeline/checklist/test4.png', 'test_info', 'test_title', promise4.id))
    db.session.add(Checklist(5, '/img/timeline/checklist/test5.png', 'test_info', 'test_title', promise4.id))

    db.session.commit()


if __name__ == '__main__':
    from . import db
    from DoMyung.models import Party, Likes, Promise, Checklist

    init_db(db, Party, Promise, Likes, Checklist)
