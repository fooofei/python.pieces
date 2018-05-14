# coding=utf-8
'''
实现  CTRL+C 或者被 kill （不同 signal） 也能正常执行某段代码
'''

import os
import sys
import time
import signal




def daemon_stop_signals(signum, frame):
    '''
    If process kill by some signals, then execute here
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

if __name__ == '__main__':
    test_kill()
