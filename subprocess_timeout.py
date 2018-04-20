#coding=utf-8


'''
this file shows subprocess's advanced usage.

'''

import datetime
import time
import timeit
import os
import subprocess

def popen_timeout_wait(popen_ins, timeout):
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


def popen_kill(popen_ins):
  '''
  kill process created by subprocess.Popen()
  :param popen_ins:
  :return:  None
  '''
  if popen_ins.poll() is None:
    #print('kill proc {}'.format(popen_ins.pid))
    # popen_ins.terminate()
    popen_ins.kill()

  while popen_ins.poll()  is None:
    #print('fail kill, trying') # will be many times
    # if too fast, will be error OSError: [Errno 3] No such process
    os.kill(popen_ins.pid, 9)
    time.sleep(3)


def timeout_subprocess(*args,**kwargs):
  '''
  when wrap subprocess.Popen() as this,
  the Popen() param will not have auto complete
  '''
  timeout=kwargs.pop('timeout',None)
  p_ins = subprocess.Popen(*args,**kwargs)

  if timeout is not None:
    if not popen_timeout_wait(p_ins,timeout):
      # timeout
      popen_kill(p_ins)
  return p_ins

def popen_isalive(p):
  return  p.poll() is None






