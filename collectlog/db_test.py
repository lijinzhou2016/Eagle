#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from new import classobj



engine = create_engine('sqlite:////Users/li_jinzhou/PycharmProjects/Eagle/collectlog/date.sqlite')
metadata = MetaData()
Base = declarative_base()

# users_table = Table('users', metadata,
#                     Column('id', Integer, primary_key=True),
#                     Column('name', String(8)),
#                     Column('fullname', String(8)),
#                     Column('password', String(8))
#                     )
#
# test_table = Table('test', metadata,
#                     Column('id', Integer, primary_key=True),
#                     Column('name', String(8)),
#                     Column('fullname', String(8)),
#                     Column('password', String(8))
#                     )
serialno = ""
def set_serialno(serial):
    global serialno
    serialno = serial

def create_db():
    global serialno
    Table("summary", metadata,
          Column('id', Integer, primary_key=True),
          )

    Table(serialno, metadata,
          Column('id', Integer, primary_key=True),
          )

    metadata.create_all(engine)


class Summary(Base):

     __tablename__ = 'summary'

     id = Column(Integer, primary_key=True)
     name = Column(String)
     fullname = Column(String)
     password = Column(String)


class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

def create_device_class():
    global serialno
    globals()[serialno] = type(serialno, (Device, ), {"__tablename__": serialno})


Session = sessionmaker(bind=engine)
session = Session()

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




