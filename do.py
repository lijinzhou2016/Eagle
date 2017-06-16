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
import subprocess
import traceback

sys.path.append(os.path.join(settings.BASE_DIR))
from collectlog import db as database
from collectlog.db import Summary, Detail




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

loop = sys.argv[1]
assistant = sys.argv[2]
log_absoulte_root_path = sys.argv[3]
case_conf_path = sys.argv[4]
case_path = sys.argv[5]
serialno = sys.argv[6]
version = sys.argv[7]
port = sys.argv[8]
assistant_serialno = sys.argv[9]
assistant_version = sys.argv[10]
assistant_port = sys.argv[11]

device_log_path = os.path.join(log_absoulte_root_path, serialno)
if assistant == "true":
    sdevice_log_path = os.path.join(device_log_path, assistant_serialno)
    os.environ.setdefault("sdeviceLogPath", sdevice_log_path)

os.environ.setdefault("deviceLogPath", device_log_path)
os.environ.setdefault("deviceName", serialno)
os.environ.setdefault("port", port)
os.environ.setdefault("assistant", assistant)
os.environ.setdefault("sdeviceName", assistant_serialno)
os.environ.setdefault("sport", assistant_port)

print "="*100
print "====", " "*40, u"开始测试", " "*40, "===="
print "="*100
print

# os.environ.setdefault("deviceName", "emulator-5554")
# os.environ.setdefault("assistant", "false")
# case_conf_path = "/Users/li_jinzhou/PycharmProjects/Eagle/pandaMTBF/config/smoke.csv"
# case_path = "/Users/li_jinzhou/PycharmProjects/Eagle/pandaMTBF"
# loop = 3
with open(case_conf_path) as f:
    cases = f.readlines()

# 创建log目录
if not os.path.exists(device_log_path):
    os.makedirs(device_log_path)
if assistant == "true":
    if not os.path.exists(sdevice_log_path):
        os.makedirs(sdevice_log_path)
time.sleep(1)
# summary

def get_device_info(cmd):
    format_cmd = "adb -s " + serialno + " shell " + cmd
    result = str(subprocess.Popen(format_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True).communicate()[0])
    return result

summary = Summary(
    id=1,
    serialno=serialno,
    sw=get_device_info("getprop ro.build.description"),
    android_version=version,
    phone_version=get_device_info("getprop ro.build.display.id"),
    gsm_baseband = get_device_info("getprop gsm.version.baseband"),
    linux_kernel = get_device_info("cat /proc/version"),
    port=port,
    release_time=get_device_info("getprop ro.build.date"),
    loop=loop,
    assistant_serialno=assistant_serialno,
    assistant_version=assistant_version,
    assistant_port=assistant_port,
    start_time_s=str(time.time()),
    start_time=log_absoulte_root_path.split("/")[-1],
    total_case=0,
    execute_case=0,
    fail=0,
    anr=0,
    crash=0,
    tombstone=0,
    log_root_path=log_absoulte_root_path
)

time.sleep(1)

detail_list=[]
for L in range(int(loop)):
    for case in cases:
        if case.strip().startswith("#"):
            continue
        case_item = case.strip().replace("\n", "").split(",")
        case_name = case_item[0]
        case_loop = case_item[1]
        case_flag = 0

        if len(case_item) > 2:
            if case_item[3] == "reboot":
                case_flag = 1
            elif case_item[3] == "assistant":
                case_flag = 2
            else:
                raise ValueError("Unknown " + case_item[3])
        for l in range(int(case_loop)):
            # print L+1,l+1,case_name
            # time.sleep(1)
            detail = Detail(
                state=0,
                flag=case_flag,
                case_name=case_name,
                big_loop=str(L+1),
                small_loop=str(l+1),
                m_log_path=os.path.join(
                    device_log_path, "LOOP_"+str(L+1), case_name.split(".")[-1], "loop_"+str(l+1), "mdevice"
                ),
                s_log_path=os.path.join(
                    device_log_path, "LOOP_"+str(L+1), case_name.split(".")[-1], "loop_"+str(l+1), "sdevice"
                )
            )
            detail_list.append(detail)


db = database.connect_db(device_log_path, serialno)
print type(db)
time.sleep(1)

db.add(summary)
# print "after add"
time.sleep(1)
db.commit()
# print "after commit"
time.sleep(1)
db.add_all(detail_list)
db.commit()
time.sleep(1)
# print "haha"
# time.sleep(1)
# for d in db.query(Detail).all():
#     # print "hhhhhhhhhh"
#     time.sleep(1)
#     print d.id, d.case_name, d.state

s = db.query(Summary).all()[0]
s.total_case=0
for d in db.query(Detail).filter(Detail.state == 0).all():
    try:
        d.state = 1
        d.start_time_s = str(time.time())
        d.start_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

        run_case_cmd = "bash " + os.path.join(settings.BASE_DIR, "cmdline.sh") + " " + case_path + " " + d.case_name
        print "="*20, d.case_name, " LOOP:", d.big_loop, " loop:", d.small_loop, "="*20, "\n"
        print "Start time:", d.start_time
        db.commit()
        # print d.m_log_path
        os.environ.pop("m_log_path", "false")
        os.environ.setdefault("m_log_path", d.m_log_path)
        # os.environ.pop("m_log_path")
        # print os.environ.get("m_log_path")
        if not os.path.exists(d.m_log_path):
            os.makedirs(d.m_log_path)

        os.system(run_case_cmd)

        d.stop_time_s = str(time.time())
        d.stop_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        d.total_time = str((float(d.start_time_s) - float(d.start_time_s)))

        # 脚本执行结果状态
        with open(os.path.join(d.m_log_path, "case.log"), 'r') as f:
            lines = f.readlines()
        for line in lines:
            if "Test Result - Pass" in line:
                d.state=2
                break
            if "Test Result - Failed" in line:
                d.state=4
        if d.state == 1:
            d.state = 4

        s.stop_time = d.stop_time
        s.stop_time_s = d.stop_time_s
        s.total_time = str(float(d.stop_time_s) - float(s.start_time_s))
        db.commit()
    except BaseException, e:
        print "case loop"
        traceback.print_exc()

