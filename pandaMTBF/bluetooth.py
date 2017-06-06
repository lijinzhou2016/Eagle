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

bt_name = "A_" + str(time.time()).split(".")[0]

class Bluetooth(frame.BaseCase):

    def __init__(self, driver, logger):
        self.logger = logger
        self.driver = driver

    def open_bluetooth(self, device):
        self.driver.find_element_by_android_uiautomator('new UiSelector().text("蓝牙")').click()
        time.sleep(2)
        # btns = self.driver.find_elements_by_id("com.meizu.connectivitysettings:id/switchWidget")
        # for btn in btns:
        #     state = btn.text()
        #     if state == "关闭":
        #         btn.click()
        #         time.sleep(3)
        #
        # for btn in btns:
        #     state = btn.text()
        #     if state == "关闭":
        #         self.logger.error("open bluetooth failed")
        #         return False
        self.logger.debug(device+": open bluetooth success")
        return True

    def rename_bluetooth(self, device):
        self.driver.find_element_by_android_uiautomator('new UiSelector().text("蓝牙名称")').click()
        time.sleep(2)
        self.driver.find_element_by_id("com.meizu.connectivitysettings:id/name").clear()
        time.sleep(1)
        self.driver.find_element_by_id("com.meizu.connectivitysettings:id/name").send_keys(bt_name)
        time.sleep(1)
        self.driver.find_element_by_android_uiautomator('new UiSelector().text("重命名")').click()
        self.logger.debug(device+": rename {0} success".format(bt_name))
        return True

    def disconnect(self, device):
        try:
            self.driver.find_element_by_id("com.meizu.connectivitysettings:id/deviceDetails").click()
            self.delay(1)
            self.driver.find_element_by_android_uiautomator('new UiSelector().text("取消配对")').click()
            time.sleep(1)
            self.logger.debug(device+": disconnected success")
            return True
        except:
            return True




class AndroidTestCases(frame.BaseCase):

    def setUp(self):
        self.driver, self.s_driver = self.init()
        self.m_bt = Bluetooth(self.driver, self.logger)
        if self.s_driver:
            self.s_bt = Bluetooth(self.s_driver, self.logger)
        try:
            self.driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
            self.s_driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
            time.sleep(1)
        except:
            pass


    def tearDown(self):
        self.clear()

    def test_connect_and_disconnect(self):
        """
        蓝牙配对与取消
        :return:
        """


        self.m_bt.open_bluetooth("mdevice")
        self.m_bt.disconnect("mdevice")
        self.s_bt.open_bluetooth("sdevice")
        self.s_bt.rename_bluetooth("sdevice")

        try:
            self.logger.debug("flush list")
            self.driver.find_element_by_id("com.meizu.connectivitysettings:id/switchWidget").click()
            self.delay(2)
            self.driver.find_element_by_id("com.meizu.connectivitysettings:id/switchWidget").click()
            self.logger.debug("wait for connect ... ")
            self.delay(8)
            self.driver.find_element_by_android_uiautomator('new UiSelector().text("{0}")'.format(bt_name)).click()

            self.delay(8)
            self.s_driver.find_element_by_android_uiautomator('new UiSelector().text("配对")').click()
        except:
            self.logger.error("connect timeout")
            self.result.fail()
            return



        self.delay(3)
        if self.driver.find_element_by_id("com.meizu.connectivitysettings:id/deviceDetails"):
            self.logger.debug("connect success")
            self.result.success()
        else:
            self.logger.debug("connect failed")
            self.result.fail()






    # def test_connected_and_send_picture(self):
    #     """
    #     蓝牙配对，主设备发送一张图片
    #     :return:
    #     """
    #     pass


