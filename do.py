#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import settings

__author__ = "LiJinzhou"
__date__ = "2017/5/6 下午10:03"


import time
import os
import sys
import multiprocessing
import settings


#gnome-terminal --maximize --tab "Phone1" -e "bash start.sh $device1 $rootFolder phone1 device1 $refdevice1" --tab "Phone2" -e "bash start.sh $device2 $rootFolder phone2 device2 $refdevice2" --tab "Phone3" -e "bash start.sh $device3 $rootFolder phone3 device3 $refdevice3" --tab "Phone4" -e "bash start.sh $device4 $rootFolder phone4 device4 $refdevice4" --tab "Phone5" -e "bash start.sh $device5 $rootFolder phone5 device5 $refdevice5" --tab "Phone6" -e "bash start.sh $device6 $rootFolder phone6 device6 $refdevice6"



with open('log.path', 'w') as f:
    f.write(settings.LOG_ABSOULTE_ROOT_PATH)


for serialno, loop in settings.DEVICES:
    pass




class Environ(object):
    def __init__(self):
        pass

    def set(self, key, value):
        os.environ.setdefault(key, value)

    def get(self, key, default=None):
        return os.environ.get(key, default)



class Config(object):
    def __init__(self, serial, root_path):
        self._serial = serial
        self._environ = Environ()
        self._case_list = settings.CASE_LIST
        self._log_root_path = settings.LOG_ROOT_PATH
        self._case_loop = settings.CASE_LOOP
        self._case_path = settings.CASE_PATH
        self._start_test_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

        self._log_absolute_path = os.path.join(root_path, self._serial)
        self._current_case_name = ""
        self._current_case_loop = ""
        self._current_time = ""
        self._case_info = {}

        self._db_path = root_path


        self._case_info = {
            "serial": self._serial,
            "start_time": self._current_time,
            "case_name": self._current_case_name,
            "case_path": os.path.join(self._case_path, self._current_case_name),
            "case_big_loop": self._case_loop,
            "case_small_loop": "",
            "case_log_path": os.path.join(self._log_absolute_path, self._current_case_name, self._current_case_loop),
            "device_log_path": "",
            "db_path": "",
            "db_name": "",
        }

    def set_db_path(self):
        self._db_path = os.path.join(self._log_root_path, )

    def get_case_info(self):
        return self._case_info

    def current_time(self):
        return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

    def log_absolute_path(self):
        return os.path.join(self._log_root_path, self.current_time(), self._serial)

def current_time(self):
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

def init(serial):
    log_root_path = "/usr/test/date/"




if __name__ == "__main__":
    serials = settings.SERIAL
    process = []

    for serial in serials:
        process.append(multiprocessing.Process(target=init, args=(serial,)))

    for p in process:
        p.start()


