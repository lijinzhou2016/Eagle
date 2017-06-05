#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess
import re

#test = r'ActivityRecord{bdd425b u0 com.yunos.camera/.CameraActivity t63}'
log = subprocess.Popen('adb shell dumpsys activity', shell=True, stdout=subprocess.PIPE).communicate()[0]

p = "(ActivityRecord{)[^}]+(\w+\s|[^}]+Activity)"
pp ="([a-zA-Z]+\.)[^}]+(\w+\s|[^}]+Activity)"

p_re = re.compile(p)
pp_re = re.compile(pp)

log = p_re.search(log).group(0)
#print log
log = pp_re.search(log).group(0).strip()
print "adb shell am start -n '%s'" %log
