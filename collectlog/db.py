#!/usr/bin/env python
# -*- coding: UTF-8 -*-


__author__ = "LiJinzhou"
__date__ = "2017/5/15 下午2:26"


import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func



Base = declarative_base()

class Summary(Base):
    """
        summary表的操作接口
    """

    __tablename__ = 'summary'

    id = Column(Integer, primary_key=True)
    serialno = Column(String)  # 设备号
    sw = Column(String)  # 软件版本
    android_version = Column(String)
    phone_version = Column(String)
    gsm_baseband = Column(String)
    linux_kernel = Column(String)
    port = Column(String)
    release_time = Column(String)  # 软件发布时间
    loop = Column(String)
    assistant_serialno = Column(String)
    assistant_version = Column(String)
    assistant_port = Column(String)
    start_time = Column(String)  # 开始测试时间
    start_time_s = Column(String)
    stop_time_s = Column(String)
    stop_time = Column(String)  # 结束测试时间
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
    flag = Column(Integer)
    case_name = Column(String)  # case 名称
    package_name = Column(String)  # 测试应用的报名
    state = Column(Integer)  # case执行的状态
    start_time = Column(String)  # 本条case开始执行时间
    start_time_s = Column(String)
    stop_time = Column(String)  # 本条case结束时间
    stop_time_s = Column(String)
    total_time = Column(String)  # 本条case测试总时长
    big_loop = Column(Integer)  # 本条case处在哪轮大循环
    small_loop = Column(Integer)  # 本条case处在哪条小循环
    m_log_path = Column(String)  # 本条case日志相对路径
    exception_info = Column(Text)  # 发生异常的异常信息
    s_log_path = Column(String)  # 发生异常时的截图路径
    exception_dev = Column(Integer)  # 发生异常的设备


class CreateDB(object):
    """
        创建数据库和表，返回一个会话对象
    """

    def __init__(self, path, data_name):
        self._path = path
        self._db_name = data_name + ".db"
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
              Column('android_version', String(8)),                  # Android版本号
              Column('phone_version', String(8)),
              Column('gsm_baseband', String(128)),
              Column('linux_kernel', String(128)),
              Column('port', String(8)),                     # appium端口号
              Column("release_time", String(32)),            # 软件发布时间
              Column("loop", String(8)),                     # 大循环
              Column('assistant_serialno', String(128)),     # 辅助机设备号
              Column('assistant_version', String(8)),        # 辅助机Android版本号
              Column('assistant_port', String(8)),           # 辅助机appium端口号

              Column('start_time_s', String(64)),  # 开始测试时间
              Column('stop_time_s', String(64)),
              Column('start_time', String(64)),                # 开始测试时间
              Column('stop_time', String(64)),                 # 结束测试时间
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
              Column('id', Integer, primary_key=True, autoincrement=True),       # id
              Column('flag', Integer, default=0),          # 重启测试标志：1 重启测试
              Column('case_name', String(128)),              # case 名称
              Column('package_name', String(32)),            # 测试应用的报名
              Column('state', Integer, default=0),           # case执行的状态
              Column('start_time', String(64)),                # 本条case开始执行时间
              Column('stop_time', String(64)),                 # 本条case结束时间
              Column('start_time_s', String(64)),  # 本条case开始执行时间
              Column('stop_time_s', String(64)),
              Column('total_time', String(8), default="0"),  # 本条case测试总时长
              Column('big_loop', Integer),                   # 本条case处在哪轮大循环
              Column('small_loop', Integer),                 # 本条case处在哪条小循环
              Column('m_log_path', String(128)),             # 本条case 主设备日志相对路径
              Column('exception_info', Text),                # 发生异常的异常信息
              Column('s_log_path', String(128)),             # 本条case 辅助设备日志相对路径
              Column('exception_dev', Integer, default=0)    # 发生异常的设备
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
    session = connect_db("/work/eaglelog/20170609113158/91QEBNB222BB", "91QEBNB222BB")
    # d1=Detail(id=1, case_name="hahahahaha")
    # session.add(d1)
    # session.commit()
    # for id, case_name in session.query(Detail.id, Detail.case_name):
    #     print id, case_name
    for d in session.query(Detail).all():
        d.state = 1
        print d.id, d.case_name,d.state
