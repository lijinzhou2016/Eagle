#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base



engine = create_engine('sqlite:////work/pj/Eagle/collectlog/test.sqlite')
metadata = MetaData()
Base = declarative_base()

users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(8)),
                    Column('fullname', String(8)),
                    Column('password', String(8))
                    )

test_table = Table('test', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(8)),
                    Column('fullname', String(8)),
                    Column('password', String(8))
                    )
metadata.create_all(engine)


class users(Base):

     __tablename__ = 'users'

     id = Column(Integer, primary_key=True)
     name = Column(String)
     fullname = Column(String)
     password = Column(String)


class test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

Session = sessionmaker(bind=engine)
session = Session()

ed_user = users(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)

for name, fullname in session.query(users.name, users.fullname):
    print name,fullname

# t = Summary(id="sdfs")

# ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
# ed_user1 = User(name='ed1', fullname='Ed Jones1', password='edspassword')
# ed_user2 = User(name='ed2', fullname='Ed Jones2', password='edspassword')
# ed_user3 = Tester(name='ed2', fullname='Ed Jones2', password='edspassword')
# session.add_all([ed_user, ed_user1, ed_user2, ed_user3])
# session.commit()

# for name, fullname in session.query(User.name, User.fullname):
#     print name


# ---------------------------------------------------------
#
# Base = declarative_base()
# class Summary(Base):
#     __tablename__ = 'user'  # 表名
#     id = Column(Integer,)
#     name = Column(String)




