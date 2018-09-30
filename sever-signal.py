#coding=utf-8

import os
import sys
import signal
import time

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


        while True:
            time.sleep(1)
            cnt += 1
    finally:
        print('passed {}'.format(cnt))

if __name__ == '__main__':
    entry()
