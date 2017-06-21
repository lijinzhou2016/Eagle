#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import unittest
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import frame


# 主设备待测app包名和activity
# 必填
appPackage = 'com.android.calculator2'
# appPackage = "com.meizu.flyme.calculator"
appActivity = ".Calculator"

# 辅助设备待测app包名和activity
# 若无辅助设备，可以为空
sappPackage = "com.android.calculator2"
sappActivity = ".Calculator"

os.environ.setdefault("appPackage", appPackage)
os.environ.setdefault("appActivity", appActivity)
os.environ.setdefault("sappPackage", sappPackage)
os.environ.setdefault("sappActivity", sappActivity)


class Module(frame.Commons):

    def press_num(self, num):
        self.driver.find_element_by_id("digit_{0}".format(num)).click()
        self.delay(1)



class AndroidTestCases(unittest.TestCase):
    def setUp(self):
        self.logger = frame.logger
        self.driver = frame.connect_driver("mdevice")
        self.method = frame.Commons(self.driver)
        self.m_cal = Module(self.driver)

    def tearDown(self):
        self.method.clear()


    def test_one_plus_one(self):

        self.logger.debug("press 1")
        self.method.find_element_by_text("1").click()
        self.method.delay(1)
        self.logger.debug("press +")
        self.method.find_element_by_text("+").click()
        self.method.delay(1)
        self.logger.debug("press 1")
        self.method.find_element_by_text("1").click()
        self.method.delay(1)
        self.logger.debug("press =")
        self.method.find_element_by_text("=").click()

        result = self.driver.find_element_by_class_name("android.widget.EditText").text
        self.logger.debug(result)

        if result == "2":
            self.method.result.success()
        else:
            self.method.result.fail()


