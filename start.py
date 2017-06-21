#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "LiJinzhou"
__date__ = "2017/5/7 上午1:16"


import os
import settings
import time
import subprocess
import re


cmd_head = 'gnome-terminal --maximize'  # 启动一个终端命令
script = os.path.join(settings.BASE_DIR, 'do.py')  # 执行脚本文件
appium = os.path.join(settings.BASE_DIR, 'appium_server.sh')  # 启动appium服务文件
conf_path = settings.CASE_CONF_LIST_PATH  # cases集配置文件路径
case_path = settings.CASE_SOURCE_PATH  # cases脚本文件路径
log_path = settings.LOG_ABSOULTE_ROOT_PATH  # 本次测试日志根目录
devices = settings.DEVICES  # 所有设备信息字典

script_cmd = cmd_head
appium_server_cmd = cmd_head

if not os.path.exists(conf_path):
    raise IOError("Filepath "+conf_path+" not exist !")
if not os.path.exists(case_path):
    raise IOError("Filepath "+case_path+" not exist !")
if len(devices) == 0:
    raise ValueError("Not config device")
if not os.path.exists(log_path):
    os.makedirs(log_path)

# 日志目录保存到临时文件
with open(os.path.join(settings.BASE_DIR, "path.tmp"), mode="w") as f:
    f.write(log_path)


for device in devices.keys():
    tab_name = device
    # 本台设备打循环次数
    loop = devices[device]["loop"]

    # 主设备信息
    assistant = devices[device]["assistant"] or "false"
    serialno = devices[device]["serialno"]
    version = devices[device]["version"]
    port = devices[device]["port"]

    # 辅助设备信息
    assistant_serialno = devices[device]["assistant_serialno"] or "0"
    assistant_version = devices[device]["assistant_version"] or "0"
    assistant_port = devices[device]["assistant_port"] or "0"

    if loop == "" or serialno == "" or version == "" or port == "":
        raise ValueError("The Value doesn't None")
    if assistant == "true" and (assistant_serialno=="" or assistant_version=="" or assistant_port==""):
        raise ValueError("The Value doesn't None")
    if assistant != "true" and assistant != "false":
        raise ValueError("assistant is a string: 'true' or 'false'")


    # 启动appium服务的命令
    appium_server_cmd += ' --tab -t "{0}_server" '.format(tab_name) \
                             + '-e "bash {0} {1} {2}"'.format(appium, port, serialno)
    if assistant == "true":
        appium_server_cmd += ' --tab -t "{0}_assistant_server" '.format(tab_name) \
                             + '-e "bash {0} {1} {2}"'.format(appium, assistant_port, assistant_serialno)


    # 执行测试脚本命令
    script_cmd += ' --tab -t "{0}" '.format(tab_name) \
        + '-e "python {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}"'.format(
        script, loop, assistant, log_path, conf_path, case_path, serialno,
        version, port, assistant_serialno, assistant_version, assistant_port)


# 启动appium前，清理appium僵尸进程
def clear_bad_appium_thread():
    bad_thread_info = subprocess.Popen("ps aux | grep appium",
                     stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     shell=True).communicate()[0]

    bad_thread_pid_list = bad_thread_info.split("\n")
    p = "\s\d+\s"
    pp = re.compile(p)

    for thread in bad_thread_pid_list:
        try:
            if thread and "grep" not in thread:
                pid = pp.search(thread).group(0).strip()
                # print "Kill bad appium process {0}".format(pid)
                os.system("kill -9 {0}".format(pid))
        except:
            pass

clear_bad_appium_thread()

print "### 开始测试 {0}".format(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
time.sleep(1)
print "### 启动appium ###"
print appium_server_cmd
print
os.system(appium_server_cmd)

time.sleep(5)
print "### 启动脚本 ###"
print script_cmd
os.system(script_cmd)