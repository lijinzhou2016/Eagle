#!/usr/bin/env python
# -*- coding: UTF-8 -*-


__author__ = "LiJinzhou"
__date__ = "2017/5/15 下午2:26"

import sys
import json
import threading
import subprocess
import os

platform = sys.platform

with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "devicesinfo.json")) as json_file:
    json_data = json.load(json_file)

assistant = json_data["info"]["assistant"]
deviceName = json_data["mdevice"]["deviceName"]
port = json_data["mdevice"]["port"]

if assistant == "true":
    sdeviceName = json_data["sdevice"]["sdeviceName"]
    sport = json_data["sdevice"]["sport"]

def sub(cmd):
    print cmd
    subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True).wait()

if platform == "darwin":
    thread=[]
    m_cmd = "node "\
            + "/Applications/Appium.app/Contents/Resources/node_modules/appium/build/lib/main.js"\
            + " --port " + port\
            + " --udid " + deviceName\
            + " --address 127.0.0.1"
    thread.append(threading.Thread(target=sub, args=(m_cmd,)))

    if assistant == "true":
        s_cmd = "node " \
                + "/Applications/Appium.app/Contents/Resources/node_modules/appium/build/lib/main.js" \
                + " --port " + sport\
                + " --udid " + sdeviceName\
                + " --address 127.0.0.1"
        thread.append(threading.Thread(target=sub, args=(s_cmd,)))

    for t in thread:
        t.start()
    for t in thread:
        t.join()

elif platform == "win32":
    pass

elif platform == "linux2":
    pass


