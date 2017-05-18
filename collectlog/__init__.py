#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import threading
import time

from androidsystemlog import *


class M(Monitor):
    """
        重写四个监控函数
    """
    def anr_handle(self, signalnum, frame):
        print "i am error"
        self.set_except_state(True)

    def crash_handle(self, signalnum, frame):
        print "i am crash"
        self.set_except_state(True)
    
    def tombstone_handle(self, signalnum, frame):
        print "i am crash"
        self.set_except_state(True)

    def reboot_handle(self, signalnum, frame):

        if DeviceSerialno.find_this_device():
            if self.get_manual_stop_state():
                print u"logcat手动停止"
            else:
                print u"logcat异常停止"
                self.lister()

        else:
            print u"设备断开连接"
            DeviceSerialno.wait_for_device()

            if self.is_device_reboot():
                if self.is_reboot_test():
                    print u"正常重启"

                else:
                    print u"异常重启"

            else:
                print u"重新连接到设备"

            self.lister()


class MyLogcat(object):

    def __init__(self, save_path):
        self._save_path = save_path
        self._main_logcat = Logcat()
        self._system_logcat = Logcat()
        self._radio_logcat = Logcat()
        self._events_logcat = Logcat()


    def start(self):
        self._main_logcat.save_logcat(buff="main", save_path=os.path.join(self._save_path, "main.logcat"))
        self._main_logcat.save_logcat(buff="system", save_path=os.path.join(self._save_path, "system.logcat"))
        self._main_logcat.save_logcat(buff="radio", save_path=os.path.join(self._save_path, "radio.logcat"))
        self._main_logcat.save_logcat(buff="events", save_path=os.path.join(self._save_path, "events.logcat"))


    def stop(self):
        self._main_logcat.stop_logcat()
        self._system_logcat.stop_logcat()
        self._radio_logcat.stop_logcat()
        self._events_logcat.stop_logcat()


class Collect(object):
    """data 字段

        serial: 设备串号
        time: 开始时间
        case_name: 脚本名称
        case_path: 脚本实际绝对路径
        case_log_path: 脚本日志绝对路径
        case_big_loop: 脚本当前大循环轮次
        case_small_loop: 脚本当前小循环轮次
        db_name: 数据库名称
        db_path: 数据库路径

    """
    def __init__(self, root_path="./", serialno=""):

        self._device_serialno = DeviceSerialno
        self._device_serialno.connected_device(self._serialno)
        self._serialno = serialno or self._device_serialno.current_device()
        self._root_path = root_path
        self._data = {}

        self._exception_handle = M(os.getpid())
        self._document = Document()
        self._mytime = Time


    def current_time(self):
        return self._mytime.get_format_time(format_time="%Y%m%d%H%M%S")

    def set_environment_variable(self, key, value):
        os.environ.setdefault(key, value)


    def logcat(self):
        while True:
            t = self.current_time()
            l = MyLogcat()
            l.start()
            time.sleep(3600)
            l.stop()


    def collect_logcat(self):
        t = threading.Thread(target=self.logcat)
        t.setDaemon(True)
        t.start()

    def create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)


    def create_path(self):
        _case_absoult_path = self._data["case_log_path"]

        self.create_dir(os.path.join(_case_absoult_path, "info"))
        self.create_dir(os.path.join(_case_absoult_path, "logcat"))


    def start(self, data):
        self._data = data
        self.create_path()

    def stop(self):
        pass

    def test(self):
        print "test import"