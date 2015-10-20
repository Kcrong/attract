from models import Party
from models import Promise
from . import domyung_bp

from .. import db

@domyung_bp.route('/add', methods=['GET', 'POST'])
def add_promise(request):
    data = request.form
    party = db.session.query(Party).filter_by(id=data['party']).first()
    p = Promise(data['title'], data['details'], party)
    db.session.add(p)
    db.session.commit()

