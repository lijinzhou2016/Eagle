#!/usr/bin/env python
# -*- coding: UTF-8 -*-


__author__ = "LiJinzhou"
__date__ = "2017/5/15 下午2:26"


import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class Summary(Base):
    """
        summary表的操作接口
    """

    __tablename__ = 'summary'

    id = Column(Integer, primary_key=True)
    serialno = Column(String)  # 设备号
    sw = Column(String)  # 软件版本
    release_time = Column(String)  # 软件发布时间
    start_time = Column(DateTime)  # 开始测试时间
    stop_time = Column(DateTime)  # 结束测试时间
    total_time = Column(String)  # 测试总耗时
    total_case = Column(Integer)  # 总case量
    execute_case = Column(Integer)  # 已执行case量
    fail = Column(Integer)  # 执行失败的case数量
    anr = Column(Integer)  # 发生anr的case数量
    crash = Column(Integer)  # 发生Crash的case数量
    tombstone = Column(Integer)  # 发生tombstone的case数量
    log_root_path = Column(String)  # 本轮测试log的相对主目录


class Detail(Base):
    """
        detail表的操作接口
    """

    __tablename__ = 'detail'

    id = Column(Integer, primary_key=True)
    case_name = Column(String)  # case 名称
    package_name = Column(String)  # 测试应用的报名
    state = Column(Integer)  # case执行的状态
    start_time = Column(DateTime)  # 本条case开始执行时间
    stop_time = Column(DateTime)  # 本条case结束时间
    total_time = Column(String)  # 本条case测试总时长
    big_loop = Column(Integer)  # 本条case处在哪轮大循环
    small_loop = Column(Integer)  # 本条case处在哪条小循环
    log_path = Column(String)  # 本条case日志相对路径
    exception_info = Column(Text)  # 发生异常的异常信息
    pic_path = Column(String)  # 发生异常时的截图路径


class CreateDB(object):
    """
        创建数据库和表，返回一个会话对象
    """

    def __init__(self, path, serialno):
        self._serialno = serialno
        self._path = path
        self._db_name = serialno + ".db"
        self._sql_path = 'sqlite:///' + os.path.join(self._path, self._db_name)
        self._engine = create_engine(self._sql_path)


    def create(self):
        metadata = MetaData()

        """
            每台设备执行case的概要信息
        """
        Table('summary', metadata,
              Column('id', Integer, primary_key=True),       # id
              Column('serialno', String(16)),                # 设备号
              Column('sw', String(64)),                      # 软件版本
              Column("release_time", String(32)),            # 软件发布时间
              Column('start_time', DateTime),                # 开始测试时间
              Column('stop_time', DateTime),                 # 结束测试时间
              Column('total_time', String(8), default="0"),  # 测试总耗时
              Column('total_case', Integer, default=0),      # 总case量
              Column('execute_case', Integer, default=0),    # 已执行case量
              Column('fail', Integer, default=0),            # 执行失败的case数量
              Column('anr', Integer, default=0),             # 发生anr的case数量
              Column('crash', Integer, default=0),           # 发生Crash的case数量
              Column('tombstone', Integer, default=0),       # 发生tombstone的case数量
              Column('log_root_path', String(16))            # 本轮测试log的相对主目录
              )


        """
            每条case的详细信息

            state:  0: standy by, 1: running, 2: pass, 3: stop
                    4: fail,  5: crash,  6: tombstone, 7: anr,  8: reboot
        """
        Table('detail', metadata,
              Column('id', Integer, primary_key=True),       # id
              Column('case_name', String(128)),              # case 名称
              Column('package_name', String(32)),            # 测试应用的报名
              Column('state', Integer, default=0),           # case执行的状态
              Column('start_time', DateTime),                # 本条case开始执行时间
              Column('stop_time', DateTime),                 # 本条case结束时间
              Column('total_time', String(8), default="0"),  # 本条case测试总时长
              Column('big_loop', Integer),                   # 本条case处在哪轮大循环
              Column('small_loop', Integer),                 # 本条case处在哪条小循环
              Column('log_path', String(128)),               # 本条case日志相对路径
              Column('exception_info', Text),                # 发生异常的异常信息
              Column('pic_path', String(128))                # 发生异常时的截图路径
              )
        metadata.create_all(self._engine)


    def connect(self):
        Session = sessionmaker(bind=self._engine)
        return Session()


def connect_db(path, serialno):
    create_db = CreateDB(path, serialno)
    create_db.create()
    return create_db.connect()


if __name__ == "__main__":
    print "beign......"
    db = connect_db("/Users/li_jinzhou/PycharmProjects/Eagle/collectlog", "hahddddaha")
