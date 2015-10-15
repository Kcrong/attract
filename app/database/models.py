# -*-coding:utf-8-*-

from sqlalchemy import Column, Integer, String, BOOLEAN

from database import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True)
    userid = Column(String(30), nullable=False, unique=False)
    password = Column(String(50), nullable=False)
    active_yn = Column(BOOLEAN(), nullable=False, default=True)

    def __init__(self, userid=None, password=None):
        self.password = password
        self.userid = userid
