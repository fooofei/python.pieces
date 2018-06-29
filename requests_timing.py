#coding=utf-8

'''
使用 requests 发请求，如何评估被请求的url吞吐量

首先安装  如果能 pip 就更好了  不能pip 就下载下面的 rpm 包
https://centos.pkgs.org/7/centos-x86_64/c-ares-1.10.0-3.el7.x86_64.rpm.html
https://centos.pkgs.org/7/centos-extras-x86_64/libev-4.15-7.el7.x86_64.rpm.html
https://centos.pkgs.org/7/centos-extras-x86_64/python-greenlet-0.4.2-4.el7.x86_64.rpm.html
https://centos.pkgs.org/7/centos-extras-x86_64/python-gevent-1.0-3.el7.x86_64.rpm.html

https://github.com/kennethreitz/grequests

请使用 taskset -c 设定CPU亲和性执行
taskset -c 10-34  python /data/tools/to-om-attack.py

其他库 
https://github.com/requests/requests-threads
https://github.com/ross/requests-futures
https://github.com/littlecodersh/trip/    

https://centos.pkgs.org/7/epel-x86_64/python2-futures-3.0.5-1.el7.noarch.rpm.html
requests_futures 是异步的，那它是协程的吗？只是在创建线程池？那创建线程池的数目能跟协程（1500）比吗？
去试试 这么想 线程也行， 线程的话他能实时响应，基于事件的协程可能会有太多中断

CentOS 离线没有 pip 的情况下安装 rpm
https://centos.pkgs.org/7/epel-x86_64/python2-futures-3.0.5-1.el7.noarch.rpm.html

grequest 和 requests-futures 讨论
https://stackoverflow.com/questions/9110593/asynchronous-requests-with-python-requests

'''
import os
import sys
import time
import json
import requests
import socket
import threading
import timeit
import itertools
import grequests
import copy
import gevent
import signal
import functools


class Count(object):
    def __init__(self):
        self.src_ip = itertools.count()
        self.stats_response = 0
        self.stats_none200 = 0
        self.stats_200 = 0
        self.stats_exception = 0
        self.stop = False

    def __str__(self):
        return 'exception={0} response={1} response-200={2} response-!200={3}'.format(
            self.stats_exception, self.stats_response, self.stats_200, self.stats_none200)


def __grequest_exp_handler(self, req, exp):
    self.stats_exception += 1
    print('{0} {1}'.format(exp, req))


def __signal_handler(*args, **kwargs):
    # 接管 Greelet 的 CTRL+C 异常
    print('catch signal {0} {1}'.format(args, kwargs))
    sys.exit(0)


def pps(requests, size, thread_func, args):
    '''
    usage:

    def __thread_func(stat):

        # refresh the stat, print it
        pass

    addr = 'http://xxxx'
    headers = {"Content-Type": "application/json"}
    data={}
    rs = (grequests.post(addr, json=data, timeout=60))
    stat = Count()
    try:
        pps(rs, 2000, thread_func=__thread_func, args=(stat,))
    finally:
        print('[+] exit at {1}'.format(stat))

    '''
    stat = args[0]
    th = threading.Thread(target=thread_func, args=args)
    th.daemon = True
    th.start()

    # 接管 Greelet 的 CTRL+C 异常
    gevent.signal(signal.SIGINT, __signal_handler)
    try:
        for r in grequests.imap(requests, size=size, exception_handler=functools.partial(__grequest_exp_handler, stat)):
            stat.stats_response +=1
            if r.status_code == 200:  # or r.content != b'{"message":"success","status":0}':
                stat.stats_200 += 1
            else:
                stat.stats_none200 += 1
                # print('[!] {0} {1}'.format(stat.stats_fail, r.content))
    finally:
        stat.stop = True
        th.join()
