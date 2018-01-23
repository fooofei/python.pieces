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

  put <files_from> to <files_to>
  :param hosts: [(ip1,port1,user1), (...)]
  :param files_from: [path1,path2, ...]
  :param files_to: [path1,path2, ...]

  '''
  import paramiko
  import itertools
  import tempfile
  from io_in_out import io_hash_fullpath
  import errno
  import stat

  hosts=[]
  files_from=[] # remote path
  files_to = [] # remote path
  client_from = paramiko.SSHClient()
  client_to = paramiko.SSHClient()

  client_from.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client_to.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  client_from.connect(*hosts[0])
  client_to.connect(*hosts[1])

  sftp_from = client_from.open_sftp()
  sftp_to = client_to.open_sftp()


  for f,t in itertools.izip(files_from, files_to):

    # test exists
    try:
      sftp_from.lstat(f)
    except IOError as er:
      print('[!] error {} {}'.format(er,f))
      continue

    tmpf = tempfile.mkstemp('_ssh')
    os.close(tmpf[0])
    tmpf = tmpf[1]
    sftp_from.get(f,tmpf)
    m = io_hash_fullpath(tmpf)
    print('[+] get {} to {} md5={}'.format(f,tmpf,m))

    # sftp_to.open(t)
    # sftp_to.lstat(t)
    # both return Errno 2 No such file

    # if exists, remove it
    try:
      sftp_to.lstat(t)
      sftp_to.remove(t)
    except IOError as er:
      if not (er.errno == errno.ENOENT):
        raise  er
    sftp_to.put(tmpf,t)

    print('[+] put to {}'.format(t))

    # add execute mode for ELF
    with open(tmpf) as fr_tmp:
      header = fr_tmp.read(4)
      if header[1::] == 'ELF':
        st = sftp_to.lstat(t)
        sftp_to.chmod(t,st.st_mode |stat.S_IEXEC)

    print('')
    os.remove(tmpf)

  client_from.close()
  client_to.close()
