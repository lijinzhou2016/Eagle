#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import sys
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 设备配置
# (serialno, loop）
DEVICES = [
    ("xxxxxx", 8),
    ("oooooo", 6)
]

# 手动配置此目录，存放日志的总目录
LOG_PATH = "/Users/li_jinzhou/PycharmProjects/Eagle/logs"

# 测试开始时间戳，作为本次测试log根目录
START_TIME = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))


# 本次测试log根目录
LOG_ABSOULTE_ROOT_PATH = os.path.join(LOG_PATH, START_TIME)

# case列表文件路径
CASE_CONF_LIST_PATH = "/config/path/list.csv"

# case文件路径
CASE_SOURCE_PATH = "/source/path"