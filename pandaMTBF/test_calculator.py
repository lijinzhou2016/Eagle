#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import frame


# 主设备待测app包名和activity
# 必填
appPackage = 'com.android.calculator2'
appActivity = ".Calculator"

# 辅助设备待测app包名和activity
# 若无辅助设备，可以为空
sappPackage = "com.android.calculator2"
sappActivity = ".Calculator"

os.environ.setdefault("appPackage", appPackage)
os.environ.setdefault("appActivity", appActivity)
os.environ.setdefault("sappPackage", sappPackage)
os.environ.setdefault("sappActivity", sappActivity)


class ModuleName(frame.DecorateDriver):

    def __init__(self, driver):
        if driver:
            self.driver = driver

    def press_num(self, num):
        self.driver.find_element_by_id("digit_{0}".format(num)).click()



class AndroidTestCases(frame.BaseCase):

    def setUp(self):
        self.driver, self.s_driver = self.init()
        self.m_module = ModuleName(self.driver)
        if self.s_driver:
            self.s_module = ModuleName(self.s_driver)


    def tearDown(self):
        self.clear()


    def test_1(self):
        self.logger.debug("keyia")

        self.driver.find_element_by_id("digit_8").click()
        self.logger.debug("press 8")

        self.driver.find_element_by_id("op_add").click()
        self.logger.debug("press +")
        self.driver.find_element_by_id("digit_5").click()
        self.logger.debug("press 5")
        self.driver.find_element_by_id("eq").click()
        self.logger.debug("press =")
        self.result.success()


    def test_2(self):
        self.m_module.press_num("1")
        self.logger.debug("device press 1")
        self.delay(1)
        self.s_module.press_num("2")
        self.logger.debug("press 2")
        self.delay(1)
        self.driver.find_element_by_id("digit_3").click()
        self.logger.debug("press 3")
        self.delay(1)
        self.s_driver.find_element_by_id("digit_4").click()
        self.logger.debug("press 4")
        self.delay(1)
        self.driver.find_element_by_id("digit_5").click()
        self.logger.debug("device press 5")
        self.delay(1)
        self.s_driver.find_element_by_id("digit_6").click()
        self.logger.debug("press 6")
        self.delay(1)
        self.driver.find_element_by_id("digit_7").click()
        self.logger.debug("press 7")
        self.delay(1)
        self.s_driver.find_element_by_id("digit_8").click()
        self.logger.debug("press 8")
        self.delay(1)
        self.result.success()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(AndroidTestCases('test_1'))
    # suite.addTest(AndroidTestCases('test_2'))
    return suite

if __name__ == "__main__":
    unittest.main()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
