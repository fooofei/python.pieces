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
        # signal.signal(9, daemon_stop_signals) #signal.SIGKILL # cannot be catch
        signal.signal(signal.SIGILL, _stop_signals)
        signal.signal(signal.SIGABRT, _stop_signals)
        signal.signal(3, _stop_signals)  # signal.SIGQUIT


        while True:
            time.sleep(1)
            cnt += 1
    finally:
        print('passed {}'.format(cnt))

if __name__ == '__main__':
    entry()
