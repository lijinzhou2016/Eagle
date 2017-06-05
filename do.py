#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import settings
import time
from collectlog import Collect

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

# loop = sys.argv[1]
# assistant = sys.argv[2]
# log_absoulte_root_path = sys.argv[3]
# case_conf_path = sys.argv[4]
# case_path = sys.argv[5]
# serialno = sys.argv[6]
# version = sys.argv[7]
# port = sys.argv[8]
# assistant_serialno = sys.argv[9]
# assistant_version = sys.argv[10]
# assistant_port = sys.argv[11]
#
# os.environ.setdefault("deviceName", serialno)
# os.environ.setdefault("assistant", assistant)
# os.environ.setdefault("sdeviceName", assistant_serialno)

print "="*100
print "====", " "*40, u"开始测试", " "*40, "===="
print "="*100
print

os.environ.setdefault("deviceName", "emulator-5554")
os.environ.setdefault("assistant", "false")
case_conf_path = "/Users/li_jinzhou/PycharmProjects/Eagle/pandaMTBF/config/smoke.csv"
case_path = "/Users/li_jinzhou/PycharmProjects/Eagle/pandaMTBF"
loop = 3
with open(case_conf_path) as f:
    cases = f.readlines()

for L in range(loop):
    for case in cases:
        case_item = case.strip().replace("\n", "").split(",")
        run_case_cmd = "bash " + os.path.join(settings.BASE_DIR, "cmdline.sh") + " " + case_path + " " + case_item[0]
        for l in range(int(case_item[1])):
            print
            print "="*20, case_item[0], " Loop:", L+1, " loop:", l+1, "="*20
            print
            os.system(run_case_cmd)
        break


