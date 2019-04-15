#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process
import json
import signal
import time
import threading
import os
# from module.sniffer import Sniffer
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

DURATION = 200

# 单例
def synchronized(func):
    func.__lock__ = threading.Lock()
 
    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)
 
    return lock_func

class Task(object):
    instance = None
    p = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        """
        :type kwargs: object
        """
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance


    def __init__(self):
        pass

    def task(self, name):
        # sniffer = Sniffer("api.welove520.com", name)
        # sniffer.capt_data()
        i=0
        while(time.time()-name < 10):
            i+=1


    def start_sniffer(self, name):
        self.start_time = time.time()
        self.p = Process(target = self.task, args = (self.start_time,), name = 'sniffer')    # 修改进程的名称为"子进程"
        self.p.start()


    def is_task_running(self):
        if self.p:
            print(self.p.is_alive())
            if time.time() - self.start_time > DURATION:
                self.p.terminate() 
                return False
            elif self.p.is_alive():
                return True
            else:
                return False
        else:
            return False

    def stop_sniffer(self):
        if self.p:
            self.p.terminate() 
