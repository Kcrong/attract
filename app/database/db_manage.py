# -*-coding:utf-8-*-

from database import init_db
from database import db_session
from sqlalchemy.exc import IntegrityError
from models import Users

init_db()


def db_user_check(get_userid, get_password):
    u = Users.query.filter_by(userid=get_userid, password=get_password, active_yn=True).first()
    if u is None:
        return False  # no user
    else:
        return u.name  # user


def db_user_add(get_userid, get_password):
    check_dep = Users.query.filter_by(userid=get_userid, active_yn=True).first()
    if check_dep is None:
        pass
    else:
        return False
    u = Users(get_userid, get_password)
    db_session.add(u)
    try:
        db_session.commit()
    except IntegrityError:  # same email
        db_session.rollback()
        return False
    return True
