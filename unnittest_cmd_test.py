#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# os.system("cd /Users/li_jinzhou/PycharmProjects/Eagle/pandaMTBF")
path = "/Users/li_jinzhou/PycharmProjects/Eagle/pandaMTBF"
case = "test_calculator.AndroidTestCases.test_1"
script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cmdline.sh")
import threading
def fun():
    os.system("bash {0} {1} {2}".format(script, path, case))

t=threading.Thread(target=fun)
t.start()
t.join()
