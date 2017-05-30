#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
import unittest
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

class BaseCase(unittest.TestCase):
    start_time = ""
    end_time = ""

    def init(self):
        sdriver = None
        driver = self.init_driver()
        if get_conf("assistant") or json_data["info"]["assistant"] == "true":
            sdriver = self.init_sdriver()
        return driver, sdriver

    def init_driver(self):
        self.logger = logger
        self.result.is_execute = 0
        desired_caps = dict()
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = get_conf("platformVersion") or json_data["mdevice"]["platformVersion"]
        desired_caps['deviceName'] = get_conf("deviceName") or json_data["mdevice"]["deviceName"]
        desired_caps['appPackage'] = get_conf("appPackage")
        desired_caps['appActivity'] = get_conf("appActivity")
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"
        url = 'http://127.0.0.1:{0}/wd/hub'.format(get_conf("port") or json_data["mdevice"]["port"])
        self.start_time = time.time()
        driver = webdriver.Remote(url, desired_caps)
        # self.decorate = DecorateDriver(self.driver)
        time.sleep(1)
        try:
            if driver.current_activity == get_conf("appActivity"):
                log.debug("Launch app Success")
            else:
                log.exception("Launch app Failed")
        except BaseException, e:
            self.logger.exception("error")
            sys.exit()
        return driver


    def init_sdriver(self):
        sdesired_caps = dict()
        sdesired_caps['platformName'] = 'Android'
        sdesired_caps['platformVersion'] = get_conf("splatformVersion") or json_data["sdevice"]["splatformVersion"]
        sdesired_caps['deviceName'] = get_conf("sdeviceName") or json_data["sdevice"]["sdeviceName"]
        sdesired_caps['appPackage'] = get_conf("sappPackage")
        sdesired_caps['appActivity'] = get_conf("sappActivity")
        sdesired_caps["unicodeKeyboard"] = "True"
        sdesired_caps["resetKeyboard"] = "True"
        surl = 'http://127.0.0.1:{0}/wd/hub'.format(get_conf("sport") or json_data["sdevice"]["sport"])
        sdriver = webdriver.Remote(surl, sdesired_caps)
        time.sleep(1)
        try:
            if sdriver.current_activity == get_conf("sappActivity"):
                log.debug("Launch app Success")
            else:
                log.exception("Launch app Failed")
        except BaseException, e:
            self.logger.exception("error")
            sys.exit()
        return sdriver


    def clear(self):
        if self.result.is_execute == 0:
            log.warn("Please give the result by self.result.success() or self.result.fail()")

        self.driver.quit()
        if self.s_driver:
            self.s_driver.quit()
        time.sleep(1)

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



class DecorateDriver(object):

    def __init__(self, driver):
        self.driver = driver


    def delay(self, t):
        time.sleep(t)
