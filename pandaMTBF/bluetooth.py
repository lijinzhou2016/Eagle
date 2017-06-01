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
appPackage = 'com.android.settings'
appActivity = ".Settings"

# 辅助设备待测app包名和activity
# 若无辅助设备，可以为空
sappPackage = 'com.android.settings'
sappActivity = ".Settings"

os.environ.setdefault("appPackage", appPackage)
os.environ.setdefault("appActivity", appActivity)
os.environ.setdefault("sappPackage", sappPackage)
os.environ.setdefault("sappActivity", sappActivity)


class Bluetooth(frame.DecorateDriver):

    def __init__(self, driver, logger):
        self.logger = logger
        self.driver = driver

    def enter_bt_view(self):
        pass






class AndroidTestCases(frame.BaseCase):

    def setUp(self):
        self.driver, self.s_driver = self.init()
        self.m_bt = Bluetooth(self.driver, self.logger)
        if self.s_driver:
            self.s_bt = Bluetooth(self.s_driver, self.logger)


    def tearDown(self):
        self.clear()


    def test_enter_bluetooth_view(self):
        """
        蓝牙配对与取消
        :return:
        """
        self.logger.debug("enter bluetooth view")
        self.driver.find_element_by_android_uiautomator('new UiSelector().text("蓝牙")').click()
        time.sleep(2)

        self.result.success()



    # def test_connected_and_send_picture(self):
    #     """
    #     蓝牙配对，主设备发送一张图片
    #     :return:
    #     """
    #     pass


