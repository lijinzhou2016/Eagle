#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
脚本编写调试阶段，启用此服务
"""

__author__ = "LiJinzhou"
__date__ = "2017/5/15 下午2:26"

import sys
import json
import threading
import subprocess
import os

platform = sys.platform

def sub(cmd):
    print cmd
    subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True).wait()


def server_start(cmd):
    thread = []
    m_cmd = cmd \
            + " --port " + port \
            + " --udid " + deviceName \
            + " --address 127.0.0.1"
    thread.append(threading.Thread(target=sub, args=(m_cmd,)))

    if assistant == "true":
        s_cmd = cmd \
                + " --port " + sport \
                + " --udid " + sdeviceName \
                + " --address 127.0.0.1"
        thread.append(threading.Thread(target=sub, args=(s_cmd,)))

    for t in thread:
        t.start()
    for t in thread:
        t.join()


with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "devicesinfo.json")) as json_file:
    json_data = json.load(json_file)

assistant = json_data["info"]["assistant"]

deviceName = json_data["mdevice"]["deviceName"]
port = json_data["mdevice"]["port"]

sdeviceName = json_data["sdevice"]["sdeviceName"]
sport = json_data["sdevice"]["sport"]

win_appium_path = json_data["info"]["win_appium_path"]
mac_appium_path = json_data["info"]["mac_appium_path"]


if platform == "darwin":
    cmd = "node " + mac_appium_path
    server_start(cmd)

elif "win32" in platform:
    cmd = "node " + win_appium_path
    server_start(cmd)

elif "linux" in platform:
    server_start("appium")


