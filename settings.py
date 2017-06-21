#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import sys
import time

# 当前路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 测试开始时间戳，作为本次测试log根目录
START_TIME = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

# 存放日志的总目录
LOG_PATH = "/work/eaglelog"

# 脚本配置文件路径
CASE_CONF_LIST_PATH = "/work/pj/Eagle/pandaMTBF/config/smoke.csv"

# 脚本路径
CASE_SOURCE_PATH = "/work/pj/Eagle/pandaMTBF"

# 本次测试log根目录
LOG_ABSOULTE_ROOT_PATH = os.path.join(LOG_PATH, START_TIME)


# 设备配置
DEVICES = {
    "device1":
    {
        "loop": "1000",
        "serialno": "022BTF7N38043454",
        "version": "4.2",
        "port": "4723",

        "assistant": "false",
        "assistant_serialno": "91QEBNB222BB",
        "assistant_version": "5.1",
        "assistant_port": "4725"
    },

    # "device2":
    # {
    #     "loop": "3",
    #     "serialno": "91QEBNB222BB",
    #     "version": "5.1",
    #     "port": "4727",
    #
    #     "assistant": "false",
    #     "assistant_serialno": "",
    #     "assistant_version": "",
    #     "assistant_port": ""
    # },

}
