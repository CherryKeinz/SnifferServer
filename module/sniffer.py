#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 网络数据包捕获与分析程序 """

import pcap
import dpkt
import json
import re
import time
from urllib import unquote
import sys
import os
import socket
from module.utils import Utils
reload(sys)
sys.setdefaultencoding('utf-8')



# req_data = ""
# times = 0
class Sniffer(object):
    def __init__(self, url, name):
        # 过滤输出目标ip
        self.dst_lists = []
        # "api.welove520.com"
        self.dst_url = url
        self.username = name
        pass


    def get_dst_ip(self):
        try:
            addrs = socket.getaddrinfo(self.dst_url, None)
            for item in addrs:
                if item[4][0] not in self.dst_lists:
                    self.dst_lists.append(item[4][0])
        except Exception as e:
            pass

    def capt_data(self):
        """
        捕获网卡数据包
        :param eth_name  网卡名，eg. eth0,eth3...
        :param p_type    日志捕获类型 1：sdk日志用例分析 2：目标域名过滤输出 3：原始数据包
        :return:
        """
        self.get_dst_ip()

        p_type = ''
        pc = pcap.pcap('eth0')
        pc.setfilter('tcp port 80')  # 设置监听过滤器
        print('start capture....')
        for p_time, p_data in pc:  # p_time为收到时间，p_data为收到数据
            if p_data:
                self.anly_capt(p_time, p_data, p_type)


    def anly_capt(self, p_time, p_data, p_type):
        """
        解析数据包
        :param p_data  收到数据
        :param p_type  日志捕获类型 1：sdk日志用例分析 2：目标域名过滤输出 3：原始数据包
        :return:
        """

        p = dpkt.ethernet.Ethernet(p_data)
        if p.data.__class__.__name__ == 'IP':
            ip_data = p.data
            src_ip = '%d.%d.%d.%d' % tuple(map(ord, list(ip_data.src)))
            dst_ip = '%d.%d.%d.%d' % tuple(map(ord, list(ip_data.dst)))
            if p.data.data.__class__.__name__ == 'TCP':
                tcp_data = p.data.data
                if dst_ip in self.dst_lists:
                    tmp = tcp_data.data.strip()
                    if len(tmp) > 0:
                        message_list = tmp.split('\r\n')
                        self.req_to_file(message_list)

    def req_to_file(self, message_list):
        """
        将请求数据转换为dic
        :param message_list:
        :return:
        """

        try:
            utils = Utils()
            utils.save_data(message_list, self.username)
        except Exception as e:
            print("error when save to file" )


