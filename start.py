#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

__author__ = "LiJinzhou"
__date__ = "2017/5/7 上午1:16"

import os
import multiprocessing
import settings
import sys
print settings.BASE_DIR
print os.path.dirname(os.path.abspath(__file__))

def run(a):
    # if a == "1":
    #     os.environ.setdefault("TEST","hello")
    #     print os.getpid()
    # else:
    print os.environ.get("TEST")
    print os.getpid()
print os.getpid()
os.environ.setdefault("TEST","hello")
t = multiprocessing.Process(target=run, args=("1",))
s = multiprocessing.Process(target=run, args=("2",))

t.start()
s.start()
# t.join()
# s.join()

# for i in range(3):
#     os.system("python do.py {0}".format(i))
