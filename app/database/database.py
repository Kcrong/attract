from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_url = 'mysql://sunrindcon:sunrindcon123@linux.kim82536.pe.kr/sunrindcon?charset=utf8'

engine = create_engine(db_url, convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
