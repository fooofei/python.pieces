#coding=utf-8

'''
这个文件用来记录模板：
一个后台服务，应该忽略哪些信号
'''

import os
import sys
import signal
import time


def daemon_stop_signals(signum, frame):
    '''
    If process kill by some signals, then execute here
    实现  CTRL+C 或者被 kill （不同 signal） 也能正常执行某段代码
    '''
    print('[+] Recv signal num={n}, daemon will exit.'.format(n=signum))
    sys.exit(0)  # this will break while

def test_kill():
    # SIGTERM is systemctrl stop sensor signal
    signal.signal(signal.SIGTERM, daemon_stop_signals)
    # SIGINT is CTRL+C
    # signal.signal(9, daemon_stop_signals) #signal.SIGKILL # cannot be catch
    signal.signal(signal.SIGILL, daemon_stop_signals)
    signal.signal(signal.SIGABRT, daemon_stop_signals)
    signal.signal(3, daemon_stop_signals)  # signal.SIGQUIT


    try:
        time.sleep(20000)
    finally:
        print("do cleanup here")


def _signal_handler(sigNum, frame):
    sys.exit(0)

def entry():
    try:
        cnt = 0
        # SIGTERM is [systemctrl stop ] signal
        signal.signal(signal.SIGTERM, _signal_handler)
        # SIGINT is CTRL+C
        signal.signal(signal.SIGINT, _signal_handler)
        # signal.signal(9, daemon_stop_signals) #signal.SIGKILL # cannot be catch
        signal.signal(signal.SIGILL, _signal_handler)
        signal.signal(signal.SIGABRT, _signal_handler)
        signal.signal(3, _signal_handler)  # signal.SIGQUIT
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

        while True:
            time.sleep(1)
            cnt += 1
    finally:
        print('passed {}'.format(cnt))

if __name__ == '__main__':
    entry()
