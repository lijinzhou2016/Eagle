#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "LiJinzhou"
__date__ = "2017/5/7 上午1:16"


import os
import multiprocessing
import settings
import sys
print settings.BASE_DIR
print os.path.dirname(os.path.abspath(__file__))

log_absoulte_root_path = settings.LOG_ABSOULTE_ROOT_PATH
if not os.path.exists(log_absoulte_root_path):
    os.makedirs(log_absoulte_root_path)

def write_file(name, msg, mode):
    with open(os.path.join(settings.BASE_DIR, name), mode=mode) as f:
        if msg:
            f.write(msg+"\n")

# 本次
write_file("path.tmp", log_absoulte_root_path, 'w')

cmd_head = 'gnome-terminal --maximize'
script_cmd = cmd_head
appium_server_cmd = cmd_head



script = os.path.join(settings.BASE_DIR, 'do.py')
appium = os.path.join(settings.BASE_DIR, 'appium_server.sh')
log_path = log_absoulte_root_path
conf_path = settings.CASE_CONF_LIST_PATH
case_path = settings.CASE_SOURCE_PATH
devices = settings.DEVICES

for device in devices.keys():
    tab_name = device
    loop = devices[device]["loop"]
    assistant = devices[device]["assistant"] or "false"
    serialno = devices[device]["serialno"]
    version = devices[device]["version"]
    port = devices[device]["port"]
    assistant_serialno = devices[device]["assistant_serialno"] or "0"
    assistant_version = devices[device]["assistant_version"] or "0"
    assistant_port = devices[device]["assistant_port"] or "0"

    if loop == "" or serialno == "" or version == "" or port == "":
        raise ValueError
    if assistant == "true" and (assistant_serialno=="" or assistant_version=="" or assistant_port==""):
        raise ValueError

    appium_server_cmd += ' --tab -t "{0}_server" '.format(tab_name) \
                             + '-e "bash {0} {1} {2}"'.format(appium, port, serialno)
    if assistant == "true":
        appium_server_cmd += ' --tab -t "{0}_assistant_server" '.format(tab_name) \
                             + '-e "bash {0} {1} {2}"'.format(appium, assistant_port, assistant_serialno)

    script_cmd += ' --tab -t "{0}" '.format(tab_name) \
        + '-e "python {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}"'.format(
        script, loop, assistant, log_path, conf_path, case_path, serialno,
        version, port, assistant_serialno, assistant_version, assistant_port)


print "="*100
print "====", " "*40, u"开始测试", " "*40, "===="
print "="*100
print

print script_cmd
print
print appium_server_cmd
os.system(appium_server_cmd)
os.system(script_cmd)