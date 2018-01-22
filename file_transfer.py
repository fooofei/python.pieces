#coding=utf-8

'''
this file shows transfer file through 3 machine.

A->B->C

B is our python script machine

'''

import os
import subprocess

def solution1():
  '''
  if machine B is linux machine, scp command is installed
  '''
  scp_path_a = 'user@ip:/path'
  scp_path_c = 'user@ip:/path'
  local_path_b = ''
  files=[]
  ret_code=-1
  for f in files:
    arg1 = os.path.join(scp_path_a,f)
    arg2 = os.path.join(local_path_b,f)
    cmds = ['scp',arg1,arg2]
    ret_code = subprocess.call(cmds)

  if ret_code==0:
    for f in files:
      arg1 = os.path.join(local_path_b,f)
      arg2 = os.path.join(scp_path_c,f)
      cmds=['scp',arg1,arg2]
      ret_code = subprocess.call(cmds)


def solution2():
  '''
  If machine B is a Windows, we call install package easy
  '''
  pass