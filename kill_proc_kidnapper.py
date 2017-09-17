# coding=utf-8

'''
only on Windows

when a process cause exception, the werfault.exe will start.

usage :
 a = multiprocessing.Process()
 a.start()

 ...
 if a.is_alive():
  kill_proc_kidnapper(a.pid)

'''

import os


def kill_proc_kidnapper(child_pid, kidnapper_name='WerFault.exe'):
  """
  关闭 进程崩溃后的 WerFault.exe 窗口
  Look among all instances of 'WerFault.exe' process for an specific one
  that took control of another faulting process.
  When 'WerFault.exe' is launched it is specified the PID using -p argument:

  'C:\\Windows\\SysWOW64\\WerFault.exe -u -p 5012 -s 68'
                           |               |
                           +-> kidnapper   +-> child_pid

  Function uses `argparse` to properly decode process command line and get
  PID. If PID matches `child_pid` then we have found the correct parent
  process and can kill it.
  """

  def taskkill(pid):
    """
    Kill task and entire process tree for this process
    """
    import subprocess
    cmd = 'taskkill /f /t /pid {0}'.format(pid)
    with open(os.devnull, 'w') as osdevnull:
      subprocess.call(cmd.split(), stdout=osdevnull)

  import argparse
  import psutil

  parser = argparse.ArgumentParser()
  parser.add_argument('-u', action='store_false', help='User name')
  parser.add_argument('-p', type=int, help='Process ID')
  parser.add_argument('-s', help='??')

  kidnapper_p = None
  child_p = None

  for proc in psutil.process_iter():
    if kidnapper_name == proc.name():
      args, unknown_args = parser.parse_known_args(proc.cmdline())

      if args.p == child_pid:
        # We found the kidnapper, aim.
        # print 'kidnapper found: {0}'.format(proc.pid)
        kidnapper_p = proc
        break

  if psutil.pid_exists(child_pid):
    child_p = psutil.Process(child_pid)

  if kidnapper_p and child_pid:
    # print 'Killing "{0}" ({1}) that kidnapped "{2}" ({3})'.format(
    #    kidnapper_p.name, kidnapper_p.pid, child_p.name, child_p.pid)
    taskkill(kidnapper_p.pid)
    return 1
  else:
    if not kidnapper_p:
      # print 'Kidnapper process "{0}" not found'.format(kidnapper_name)
      pass
    if not child_p:
      # print 'Child process "({0})" not found'.format(child_pid)
      pass
  return 0
