#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "LiJinzhou"
__date__ = "2017/5/7 上午1:16"


import os
import settings
import time


def write_file(name, msg, mode):
    with open(os.path.join(settings.BASE_DIR, name), mode=mode) as f:
        f.write(msg+"\n")

cmd_head = 'gnome-terminal --maximize'
script_cmd = cmd_head
appium_server_cmd = cmd_head
script = os.path.join(settings.BASE_DIR, 'do.py')
appium = os.path.join(settings.BASE_DIR, 'appium_server.sh')
conf_path = settings.CASE_CONF_LIST_PATH
case_path = settings.CASE_SOURCE_PATH
log_path = settings.LOG_ABSOULTE_ROOT_PATH
devices = settings.DEVICES

if not os.path.exists(conf_path):
    raise IOError("Filepath "+conf_path+" not exist !")
if not os.path.exists(case_path):
    raise IOError("Filepath "+case_path+" not exist !")
if len(devices) == 0:
    raise ValueError("Not config device")
if not os.path.exists(log_path):
    os.makedirs(log_path)

# 日志目录保存到临时文件
write_file("path.tmp", log_path, 'w')

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
        raise ValueError("The Value doesn't None")
    if assistant == "true" and (assistant_serialno=="" or assistant_version=="" or assistant_port==""):
        raise ValueError("The Value doesn't None")
    if assistant != "true" and assistant != "false":
        raise ValueError("assistant is a string: 'true' or 'false'")

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
time.sleep(5)
os.system(script_cmd)