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



time.sleep(1)

"""
sys.argv:

 1: loop
 2: assistant
 3: log_absoulte_root_path
 4: CASE_CONF_LIST_PATH
 5: CASE_SOURCE_PATH
 6: serialno
 7: version
 8: port
 9: assistant_serialno
10: assistant_version
11: assistant_port

"""
print "="*100
print "====", " "*40, u"开始测试", " "*40, "===="
print "="*100
print
for i in range(1, 12):
    print sys.argv[i]
time.sleep(15)


