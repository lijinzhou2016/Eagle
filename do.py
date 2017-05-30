#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import settings
import time
__author__ = "LiJinzhou"
__date__ = "2017/5/6 下午10:03"


import time
import os
import sys
import multiprocessing
import settings

print sys.argv[1]
print sys.argv[2]
print sys.argv[3]
print sys.argv[4]

time.sleep(5)


# xxxxxx
# 8
# /config/path/list.csv
# /source/path
# /Users/li_jinzhou/PycharmProjects/Eagle/logs/20170522095652"


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
    script_conf = {
        "serial": sys.argv[1],
        "loop": sys.argv[2],
        "case_list_path": sys.argv[3],
        "case_path": sys.argv[4],
        "log_path": sys.argv[5]
    }
    print script_conf



