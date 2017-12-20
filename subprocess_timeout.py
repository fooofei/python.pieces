#coding=utf-8


'''
this file shows subprocess's advanced usage.

'''

import datetime
import time
import timeit

def popen_timeout(popen_ins, timeout):
  '''
  :param popen_ins: the return value of subprocess.Popen()
  :param timeout:
  :return: True for finish in time, False for run out time.
  '''

  start = timeit.default_timer()

  while popen_ins.poll() is None: # is alive
    time.sleep(0.5)
    now = timeit.default_timer()
    #now = datetime.datetime.now()
    #if(now-start).seconds > timeout:
    if (now - start)>timeout:
      return False
  return True






