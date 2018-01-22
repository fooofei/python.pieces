
#coding=utf-8
import os

def env_exists(exe_test):
  '''
  测试环境变量中是否存在
  :param exe_test: 要判断的命令
  :return: True / False
  '''
  import subprocess
  try:
    with open(os.devnull) as devnull:
      p = subprocess.Popen([exe_test, u'--version'], stdout=devnull, stderr=devnull)
      p.wait()
    return True
  except OSError:
    return False


