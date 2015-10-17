from models import Users
from .. import db


def db_user_check(get_userid, get_password):
    u = Users.query.filter_by(userid=get_userid, password=get_password, active_yn=True).first()
    if u is None:
        return False
    else:
        return True


def db_user_add(get_userid, get_password):
    u = Users(userid=get_userid, password=get_password)
    db.session.add(u)
    db.session.commit()
    return True


def db_add_fb_info(get_fb_info):
    u = Users(fb_id=get_fb_info.data['id'], name=get_fb_info.data['name'])
    db.session.add(u)
    db.session.commit()
    return True


def db_fb_user_check(get_fb_id):
    return Users.query.filter_by(fb_id=get_fb_id, active_yn=True).first()
