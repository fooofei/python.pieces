# coding=utf-8
'''
1 如何向子进程发送数据 subprocess.communicate

2 subprocess.Popen, shell 参数:
            shell = False (default) , 执行参数应该是 list, 封装为 [<待执行二进制>, <arg0>,<arg1>,...]
                    更加 Pythonic 的使用方式，对执行参数更好控制
            shell = True, 执行参数可以是 str, 可以传递 '{} {} {}'.format(<待执行二进制>, <arg0>,<arg1>)
                把整个字符串直接在 shell 执行，容易被利用

3 执行参数中 escape 相关: pipes.quote()


'''

import os
import subprocess


def amr2avi():
  '''
  amr 批量转换为 avi
  此函数可以学习


  :return:
  '''
  pathf = r''
  runexe = r''
  for e in os.listdir(pathf):
    if e.endswith('.amr'):
      cmd = '{0} {1}'.format(runexe, os.path.join(pathf, e))
      # no wait
      p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
      p.communicate(input='\n')  # 这里需要向子进程中填入 \n 来继续运行，是因为子程序是这样写的


def _exec_check_output(*args, **kwargs):
  ''' such as run _exec_check_output(['svn', 'up'],stderr=subprocess.STDOUT) '''
  v = subprocess.check_output(*args, **kwargs)
  v = v.rstrip()
  v = v.decode('utf-8')
  return v


if __name__ == '__main__':
  amr2avi()
