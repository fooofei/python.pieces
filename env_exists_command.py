
#coding=utf-8
import os

def env_exists(exe_test):
  '''
  测试环境变量中是否存在
  通过无公害的 --version 来判断
  后来我又学到了一个，是使用 command -v <exe> 来判断
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


