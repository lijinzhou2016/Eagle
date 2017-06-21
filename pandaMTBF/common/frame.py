#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
from appium import webdriver
import time
import json
from mylogging import log
logger = log

def load(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        return data

json_data = load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "devicesinfo.json"))

def get_conf(key):
    return os.environ.get(key)

# print json_data["mdevice"]["deviceName"]
# print json_data["mdevice"]["port"]


# print "mdevice:", get_conf("deviceName"), get_conf("port")
# if get_conf("assistant") == "true":
#     print "sdevice:", get_conf("sdeviceName"), get_conf("sport")
# print



class Commons(object):
    start_time = ""
    end_time = ""

    def __init__(self, driver):
        self.driver = driver
        self.logger = logger

    def find_element_by_text(self, text):
        return self.driver.find_element_by_android_uiautomator('new UiSelector().text("{0}")'.format(text))


    def clear(self):
        if self.result.is_execute == 0:
            log.warn("Please give the result by self.result.success() or self.result.fail()")
        self.driver.quit()


    class result(object):
        is_execute = 0

        @classmethod
        def success(cls):
            log.info("Test Result - Pass")
            cls.is_execute += 1

        @classmethod
        def fail(cls):
            log.error("Test Result - Failed")
            cls.is_execute += 1

    def delay(self, t):
        time.sleep(t)


class ConnectDriver(object):
    def __init__(self, device):
        self.logger = logger
        if device is not None and device not in ["mdevice", "sdevice"]:
            raise ValueError("device value must 'mdevice' or 'sdevice'")

        if device == "mdevice":
            desired_caps = dict()
            desired_caps['platformName'] = 'Android'
            desired_caps['platformVersion'] = get_conf("platformVersion") or json_data["mdevice"]["platformVersion"]
            desired_caps['deviceName'] = get_conf("deviceName") or json_data["mdevice"]["deviceName"]
            desired_caps['appPackage'] = get_conf("appPackage")
            desired_caps['appActivity'] = get_conf("appActivity")
            desired_caps["unicodeKeyboard"] = "True"
            desired_caps["resetKeyboard"] = "True"
            url = 'http://127.0.0.1:{0}/wd/hub'.format(get_conf("port") or json_data["mdevice"]["port"])
            self.driver = webdriver.Remote(url, desired_caps)
            # print "wait"
            time.sleep(1)

        if device == "sdevice":
            sdesired_caps = dict()
            sdesired_caps['platformName'] = 'Android'
            sdesired_caps['platformVersion'] = get_conf("splatformVersion") or json_data["sdevice"]["splatformVersion"]
            sdesired_caps['deviceName'] = get_conf("sdeviceName") or json_data["sdevice"]["sdeviceName"]
            sdesired_caps['appPackage'] = get_conf("sappPackage")
            sdesired_caps['appActivity'] = get_conf("sappActivity")
            sdesired_caps["unicodeKeyboard"] = "True"
            sdesired_caps["resetKeyboard"] = "True"
            surl = 'http://127.0.0.1:{0}/wd/hub'.format(get_conf("sport") or json_data["sdevice"]["sport"])
            self.driver = webdriver.Remote(surl, sdesired_caps)
            # print "wait"
            time.sleep(1)

    def get_driver(self):
        return self.driver


def connect_driver(device):
    connect = ConnectDriver(device)
    return connect.get_driver()

