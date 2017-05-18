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

#gnome-terminal --maximize --tab "Phone1" -e "bash start.sh $device1 $rootFolder phone1 device1 $refdevice1" --tab "Phone2" -e "bash start.sh $device2 $rootFolder phone2 device2 $refdevice2" --tab "Phone3" -e "bash start.sh $device3 $rootFolder phone3 device3 $refdevice3" --tab "Phone4" -e "bash start.sh $device4 $rootFolder phone4 device4 $refdevice4" --tab "Phone5" -e "bash start.sh $device5 $rootFolder phone5 device5 $refdevice5" --tab "Phone6" -e "bash start.sh $device6 $rootFolder phone6 device6 $refdevice6"

device_init_info = []

with open('log.path', mode='w') as f:
    f.write(log_absoulte_root_path)


for serialno, loop in settings.DEVICES:
    device_init_info.append(
        {
            "serialno": serialno,
            "loop": loop,
            "case_list_path": settings.CASE_CONF_LIST_PATH,
            "case_path": settings.CASE_SOURCE_PATH,
            "log_absoulte_root_path": log_absoulte_root_path
        }
    )

start_cmd = "gnome-terminal --maximize"
for info in device_init_info:
    start_cmd += " --tab '{0}' ".format(info['serialno']) + "python do.py {0}".format(str(info))
print start_cmd
# os.system(start_cmd)