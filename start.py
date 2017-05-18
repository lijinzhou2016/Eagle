#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "LiJinzhou"
__date__ = "2017/5/7 上午1:16"

import os
import multiprocessing
import settings
import sys
print settings.BASE_DIR
print os.path.dirname(os.path.abspath(__file__))

log_absoulte_root_path = settings.LOG_ABSOULTE_ROOT_PATH

with open('log.path', mode='w') as f:
    f.write(log_absoulte_root_path)


start_cmd = 'gnome-terminal --maximize'
script = os.path.join(settings.BASE_DIR, 'do.py')
for serialno, loop in settings.DEVICES:
    start_cmd += ' --tab -t "{0}" '.format(serialno) \
                 + '-e "python {0} {1} {2} {3} {4} {5}"'.format(
            script, serialno, loop, settings.CASE_CONF_LIST_PATH, settings.CASE_SOURCE_PATH, log_absoulte_root_path)



print start_cmd

os.system(start_cmd)