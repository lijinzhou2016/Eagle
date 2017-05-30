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
if not os.path.exists(log_absoulte_root_path):
    os.makedirs(log_absoulte_root_path)

def write_file(name, msg, mode):
    with open(os.path.join(settings.BASE_DIR, name), mode=mode) as f:
        if msg:
            f.write(msg+"\n")

write_file("path.tmp", log_absoulte_root_path, 'w')

cmd_head = 'gnome-terminal --maximize'
start_cmd = cmd_head
cmd_list = []
script = os.path.join(settings.BASE_DIR, 'do.py')

for serialno, loop in settings.DEVICES:
    start_cmd += ' --tab -t "{0}" '.format(serialno) \
                 + '-e "python {0} {1} {2} {3} {4} {5}"'.format(
            script, serialno, loop, settings.CASE_CONF_LIST_PATH, settings.CASE_SOURCE_PATH, log_absoulte_root_path)

    tmp_cmd = cmd_head + ' --tab -t "{0}" '.format(serialno) \
                       + '-e "python {0} {1} {2} {3} {4} {5}"'.format(
            script, serialno, loop, settings.CASE_CONF_LIST_PATH, settings.CASE_SOURCE_PATH, log_absoulte_root_path)
    write_file(serialno+".sh", tmp_cmd, "w")
    cmd_list.append(tmp_cmd)

print "="*100
print "====", " "*40, u"开始测试", " "*40, "===="
print "="*100
print
print u"若某台设备异常终止，请执行以下相应命令"
for cmd in cmd_list:
    print cmd
print

print u"若发生断电等异常，所有设备全部停止，请执行以下命令继续测试"
print start_cmd
write_file("restart.sh", start_cmd, "w")
os.system("chmod 777 " + os.path.join(settings.BASE_DIR, "*.sh"))
print

print u"生成报告，请执行以下命令"
print u"此命令正在开发过程中，请耐心等待........"

# os.system(start_cmd)