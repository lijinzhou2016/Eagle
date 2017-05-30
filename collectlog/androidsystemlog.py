#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ===============================================================
#
# :Author: Li Jinzhou
# :E-mail: 414820128@qq.com
# :Version: 1.0
# :Requires: Python 2.7  ADB 1.0.39 +
# :License: this is free software, Welcome to exchange learning, supplementary optimization
#
# ---------------------------------------------------------------

import os
import subprocess
import time
import signal
import threading
import json



# 当前设备号
serialno = ""
# 格式化当前设备号：" -s xxxxxxxx "
format_serialno = ""

__all__ = ["DeviceSerialno", "Execute", "DumpsysInfo", "PullLog", "Monitor",
           "Time", "Logcat", "get_platform_name", "Document"]


class DeviceSerialno(object):
    
    """
        connected_device(device="xxxxxxxx"):  首先调用，链接设备，初始化serialno
        
        device_boot_stamp():  获取设备开机时间戳
        device_pid():  获取系统进程号
        format_device_boot_stamp():  格式化开机时间戳，如 2017-05-04 18:21:33
        get_serialno():  返回当前连接的所有设备serial列表 如 ["xxxxxx", "oooooo"]
        find_this_device():  检查当前设备是否在线, return  True: online, False: offline
        wait_for_device():  等待设备的链接, count=40000: 默认等待尝试链接40000次，大概一周时间
    
    """

    @classmethod
    def current_device(cls):
        global serialno
        return serialno
    
    
    @classmethod
    def _execute(cls, cmd):
        return subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True).communicate()[0]
    
    @classmethod
    def _set_serialno(cls, device=""):
        global serialno
        global format_serialno
        
        serialno = device
        if serialno:
            format_serialno = "-s " + serialno
            
    @classmethod
    def device_boot_stamp(cls):  # 设备启动时的时间戳
        global format_serialno
        _cmd = "adb " + format_serialno + " shell cat  /proc/uptime"
        return float(Time.get_time_stamp()) - float(cls._execute(_cmd).split(" ")[0])


    @classmethod
    def device_pid(cls):
        global format_serialno
        _cmd = "adb " + format_serialno + " shell ps system_server | awk 'NR==2{print $2}'"
        return cls._execute(_cmd)
 
    @classmethod
    def format_device_boot_stamp(cls):  # 格式化设备启动时的时间戳
        return Time.format_stamp(cls.device_boot_stamp(), format_time="%Y-%m-%d %H:%M:%S")

    @classmethod
    def get_serialno(cls):
        """
        
        :return: 当前连接的所有设备serial列表
        """
        # 'List of devices attached\nemulator-5556\tdevice\nemulator-5554\tdevice\n\n'
        serialno_list = []
        try:
            for line in cls._execute("adb devices").split("\n"):
                if "\tdevice" in line:
                    serialno_list.append(line.split("\t")[0])
        except Exception as e:
            print e
        finally:
            return serialno_list
        
        
    @classmethod
    def find_this_device(cls):  # 检查当前设备是否在线
        return serialno in cls.get_serialno()
        
        
    @classmethod
    def connected_device(cls, device=""):
        global serialno
        global format_serialno

        cls._set_serialno(device=device)
        cls.wait_for_device()
        
            
    @classmethod
    def wait_for_device(cls, count=40000):
        global serialno
        global format_serialno
        
        for c in range(count):
            connected_devices = cls.get_serialno()
            
            if serialno == "":  # 初始化时，没有指定serial
                if len(connected_devices) == 0:
                    print "wait for device",
                
                if len(connected_devices) == 1:
                    cls._set_serialno(device=connected_devices[0])
                    print "connected device ", serialno
                    return True

                if len(connected_devices) > 0:
                    print u"请指定设备serialno，或拔出多余设备",
                
            else:   # 初始化时，指定了serial
                if serialno in connected_devices:
                    print "connected device ", serialno
                    return True
                else:
                    print "wait for device ", serialno,

                
            for t in range(15):
                print ".",
                time.sleep(1)
            print


class Execute(object):

    def execute_command(self, cmd_line):
        print cmd_line
        self._child_process = subprocess.Popen(cmd_line, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        self._stdout = self._child_process.stdout
        self._stderr = self._child_process.stderr

    def wait_for_execute(self):
        self._child_process.wait()

    def stop_child_process(self):
        self._child_process.kill()

    def stdout(self):
        return self._stdout
    
    def stderr(self):
        return self._stderr

    def read_stdout(self):
        return self._child_process.communicate()[0]

    def read_stderr(self):
        return self._child_process.communicate()[1]

    def is_child_over(self):
        # return True  子线程结束
        # return False 子线程正在运行

        return self._child_process.poll() is not None

  
class PullLog(object):
    
    def __init__(self):
        self._execute = Execute()
        self._anr_path = "/data/anr"
        self._crash_path = "/data/system/dropbox"
        self._tombstone_path = "/data/tombstones"
        self._pic_path = "/data/local/tmp"

    def _do_cmd(self, cmd):
        self._execute.execute_command(cmd)
        self._execute.wait_for_execute()

    def pull(self, save_path, error_path):
        _pull_cmd = "adb " + format_serialno + " pull " + error_path + " " + save_path
        self._do_cmd(_pull_cmd)

    def clear(self, error_path):
        _clear_cmd = "adb " + format_serialno + " shell rm -rf " + error_path
        self._do_cmd(_clear_cmd)

    def pull_anr(self, save_path="./"):
        self.pull(save_path, self._anr_path)
        self.clear(self._anr_path)

    def pull_crash(self, save_path="./"):
        self.pull(save_path, self._crash_path)
        self.clear(self._crash_path)

    def pull_tombstone(self, save_path="./"):
        self.pull(save_path, self._tombstone_path)
        self.clear(self._tombstone_path)

    def pull_pic(self, save_path="./"):
        _stamp = Time.get_format_time(format_time="%Y%m%d%H%M%S")
        _tmp_pic_pathname = self._pic_path + _stamp + ".png"

        _screenshot_cmd = "adb " + format_serialno + " shell screencap -p " + _tmp_pic_pathname

        self._do_cmd(_screenshot_cmd)
        self.pull(save_path, _tmp_pic_pathname)
        self.clear(_tmp_pic_pathname)


class DumpsysInfo(object):
    """
        cmd: meminfo, cpuinfo ...

        eg:
        test = DumpsysInfo("activity")
        print test.get()
        test.save()
    """

    def __init__(self):
        self._execute = Execute()

 
    def get(self, cmd=""):
        _format_dump_cmd = "adb " + format_serialno + " shell dumpsys " + cmd
        self._execute.execute_command(_format_dump_cmd)
        return self._execute.read_stdout()


    def save(self, cmd="", save_path="./", save_name="dumpinfo.txt"):
        try:
            with open(os.path.join(save_path, save_name), 'w') as f:
                f.write(self.get(cmd=cmd))
        except BaseException, e:
            print "save dumpsys {0} failed".format(cmd)
            print e


class Monitor(object):
    """
        继承此类
        重写crash_handle, anr_handle, tombstone_handle, reboot_handle 四个方法
        lister()  开始监听
        stop_lister()  停止监听
        restart_lister()  重新开始监听
        
    """

    
    def __init__(self, pid=os.getpid()):
        self._execute = Execute()
        self._logcat = Logcat()
        self._pull = PullLog()
        self._pid = pid
        self._anr_signal = signal.SIGUSR1
        self._crash_signal = signal.SIGUSR2
        self._reboot_signal = signal.SIGSEGV
        self._tombstones_signal = signal.SIGTERM
        
        self._anr_key = "ANR in"
        self._crash_key = "FATAL EXCEPTION: main"
        self._tombstones_key = "Fatal signal"
        self._reboot_test_flag_key = "REBOOT_TEST_KEY"
        
        self._is_produce_exception = False
        self._connect_state = True
        self._is_manual_stop = False
        self._device_boot_stamp = 0.0
        self._device_pid = 0
        
        
    def get_except_state(self):
        return self._is_produce_exception
    
    def set_except_state(self, state):
        self._is_produce_exception = state
        
    def set_connect_state(self, state):
        self._connect_state = state
        
    def get_connect_state(self):
        return self._connect_state
    
    def set_manual_stop_state(self, state):
        self._is_manual_stop = state
        
    def get_manual_stop_state(self):
        return self._is_manual_stop

    def set_device_pid(self):
        self._device_pid = DeviceSerialno.device_pid()

    def get_device_pid(self):
        return self._device_pid

    def set_device_boot(self):
        self._device_boot_stamp = DeviceSerialno.device_boot_stamp()

    def get_device_boot(self):
        return self._device_boot_stamp


    # ANR 处理函数
    def anr_handle(self, signalnum, frame):
        print "ANR ERROR"
        self.set_except_state(False)
        
    # Tombstone 处理函数
    def tombstone_handle(self, signalnum, frame):
        print "Tombstone ERROR"
        self.set_except_state(False)
        self._pull.pull_crash("/Users/li_jinzhou/PycharmProjects/Eagle/collectlog")

    # Crash 处理函数
    def crash_handle(self, signalnum, frame):
        print "Crash ERROR"
        self.set_except_state(False)

    # Reboot 处理函数
    def reboot_handle(self, signalnum, frame):

        if DeviceSerialno.find_this_device():
            if self.get_manual_stop_state():
                print u"logcat手动停止"
            else:
                print u"logcat异常停止"
                self.lister()

        else:
            print u"设备断开连接"
            DeviceSerialno.wait_for_device()

            if self.is_device_reboot():
                if self.is_reboot_test():
                    print u"正常重启"

                else:
                    print u"异常重启"

            else:
                print u"重新连接到设备"

            self.lister()


    # 设备是否发生了重启
    def is_device_reboot(self):
        return self.get_device_boot() - DeviceSerialno.device_boot_stamp() > 10 or \
               self.get_device_pid() != DeviceSerialno.device_pid()

    # 是否在做重启测试
    def is_reboot_test(self):
        return os.environ.get(self._reboot_test_flag_key, "False") == "True"
        
    def lister(self):
        self.set_connect_state(True)
        self.set_except_state(False)
        self.set_manual_stop_state(False)
        self.set_device_pid()
        self.set_device_boot()
        
        self._register()
        thread = threading.Thread(target=self._parser)
        thread.setDaemon(True)
        thread.start()
        
        
    def stop_lister(self):
        self._logcat.stop_logcat()
        if self._logcat.is_logcat_over():
            self.set_manual_stop_state(True)
        
    def restart_lister(self):
        self.stop_lister()
        self.lister()

    def _register(self):
        signal.signal(self._anr_signal, self.anr_handle)
        signal.signal(self._crash_signal, self.crash_handle)
        signal.signal(self._reboot_signal, self.reboot_handle)
        signal.signal(self._tombstones_signal, self.tombstone_handle)
        
        
    def _parser(self):
        self._logcat.clear_buff()
        self._logcat.start_logcat()
        logcatout = self._logcat.get_logcat_stdout()
        
        while True:
            line = logcatout.readline()
            
            if self._anr_key in line:  # 发生anr，发信号给主线程
                print "anr"
                self.set_connect_state(True)
                os.kill(self._pid, self._anr_signal)

            if self._crash_key in line:  # 发生Crash，发信号给主线程
                self.set_connect_state(True)
                os.kill(self._pid, self._crash_signal)
                
            if self._tombstones_key in line:  # tombstone
                self.set_except_state(True)
                
            if self._logcat.is_logcat_over():  # 手机断链或重启，发信号给主线程
                time.sleep(1)
                if not DeviceSerialno.find_this_device():
                    self.set_connect_state(False)
                os.kill(self._pid, self._reboot_signal)
                break


class Logcat(object):
    """
    buff :       radio, system, events, main, crash
    formatput :  brief, process, tag, raw, time, thread, long

    """
    
    def __init__(self):
        self._execute = Execute()

    def _format_logcat_cmd(self, buff="all", format_put="threadtime"):
        return "adb " + format_serialno + " logcat " + " -v " + format_put + " -b " + buff

    def start_logcat(self, buff="all", format_put="threadtime"):
        self._execute.execute_command(self._format_logcat_cmd(buff=buff, format_put=format_put))

    def get_logcat_stdout(self):
        return self._execute.stdout()

    def save_logcat(self, buff="all", save_path="./logcat.txt", format_put="threadtime"):
        _save_logcat = self._format_logcat_cmd(buff=buff, format_put=format_put) + " > " + save_path
        self._execute.execute_command(_save_logcat)

    def stop_logcat(self):
        self._execute.stop_child_process()
        self._execute.wait_for_execute()
        try:
            # 调用 save_logcat()时，不知道为什么会多产生一个线程，清理此线程
            # os.system("kill " + str(os.getpid() + 2))
            os.system("kill " + str(os.getpid() + 3))
        except Exception as e:
            pass

    def clear_buff(self):
        _claar_buff_cmd = "adb " + format_serialno + " logcat -c -b all"
        self._execute.execute_command(_claar_buff_cmd)
        self._execute.wait_for_execute()

    def is_logcat_over(self):
        return self._execute.is_child_over()


class Document(object):
    
    def create_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def get_html_files(self, filepath):
        return self.get_kind_file(filepath, ".html")

    def get_xml_files(self, filepath):
        return self.get_kind_file(filepath, ".xml")
    
    def get_json_files(self, filepath):
        return self.get_kind_file(filepath, ".json")
    
    def get_kind_file(self, filepath, kind):
        kind_files = []
        all_files = self.get_all_files(filepath)
        
        if all_files is None:
            return None

        for file in all_files:
            if kind in file:
                kind_files.append(file)
        return kind_files


    def get_all_files(self, filepath):
        if os.path.exists(filepath):
            return os.listdir(filepath)
        else:
            print "not exists: {0}".format(filepath)
            return None

    
    def load_json(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data

    
    def store_json(self, filename, data):
        with open(filename, 'w+') as json_file:
            json_file.write(json.dumps(data))

    # 字节bytes转化kb\m\g
    def format_size(self, bytes):
        try:
            bytes = float(bytes)
            kb = bytes / 1024
        except:
            print u"传入的字节格式不对"
            return "Error"
    
        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%fG" % (G)
            else:
                return "%fM" % (M)
        else:
            return "%fkb" % (kb)

    # 获取文件大小
    def get_doc_size(self, path):
        try:
            size = os.path.getsize(path)
            return self.format_size(size)
        except Exception as err:
            print(err)


class Time(object):

    @classmethod
    def get_time_stamp(cls):  # 获取当前时间戳
        return time.time()

    @classmethod
    def __format_time_stamp(cls):
        return time.localtime(cls.get_time_stamp())

    @classmethod
    def get_format_time(cls, format_time='%H:%M:%S'):  # 自定义格式化当前时间和日期
        return time.strftime(format_time, cls.__format_time_stamp())

    @classmethod
    def get_current_time(cls):  # 格式化当前时间
        return cls.get_format_time('%H:%M:%S')

    @classmethod
    def get_current_date(cls):  # 格式化当前日期
        return cls.get_format_time('%Y-%m-%d')
    
    @classmethod
    def format_stamp(cls, time_stamp, format_time="%H:%M:%S"):  # 格式化一个时间戳
        return time.strftime(format_time, time.localtime(time_stamp))

    @classmethod
    def timer(cls, func, timeout):
        threading.Timer(timeout, func).start()


class MTK(object):
    pass


class Qualcomm(object):
    pass


def get_platform_name():
    pipe = os.popen("adb " + format_serialno + " shell getprop ro.hardware")
    if "mt" in pipe:
        return "MTK"
    elif "qcom" in pipe or "msm" in pipe:
        return "Qualcomm"
    else:
        print pipe
        return "Unknown"

 

if __name__=="__main__":
    # 测试监控接口
    os.environ.setdefault("REBOOT_TEST_FLAG", "True")
    DeviceSerialno.connected_device(device="emulator-5554")
    h = Monitor()
    h.lister()
    print os.getpid()

    while True:
        time.sleep(3)
        print "Test Running: ", time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))


