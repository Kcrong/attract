from .. import db
from models import Users


def db_user_check(get_userid, get_password):
    u = Users.query.filter_by(userid=get_userid, password=get_password, active_yn=True).first()
    if u is None:
        return False
    else:
        return True
