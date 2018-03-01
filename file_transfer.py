# coding=utf-8

'''
this file shows transfer file through 3 machine.

A->B->C

B is our python script machine

'''

import os
import subprocess
import contextlib


def solution1():
  '''
  if machine B is linux machine, scp command is installed
  '''
  scp_path_a = 'user@ip:/path'
  scp_path_c = 'user@ip:/path'
  local_path_b = ''
  files = []
  ret_code = -1
  for f in files:
    arg1 = os.path.join(scp_path_a, f)
    arg2 = os.path.join(local_path_b, f)
    cmds = ['scp', arg1, arg2]
    ret_code = subprocess.call(cmds)

  if ret_code == 0:
    for f in files:
      arg1 = os.path.join(local_path_b, f)
      arg2 = os.path.join(scp_path_c, f)
      cmds = ['scp', arg1, arg2]
      ret_code = subprocess.call(cmds)


@contextlib.contextmanager
def open_remote(host):
  import paramiko

  '''
  :param host: (ip,port,username,<password>)
  :return: SSHClient instance paramiko.sftp_client.SFTPClient
  '''
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(*host)
  sftpv = client.open_sftp()

  try:
    yield sftpv
  finally:
    sftpv.close()
    client.close()


def solution2(hosts, files):
  '''
  If machine B is a Windows, we call install package easy

  put <files_from> to <files_to>
  :param hosts:  [(ip1,port1,user1), (ip2,port2,user2)]
  :param files: [(file1_from,file1_to),(file2_from,file2_to),...]
  :return:
  '''

  import paramiko
  import itertools
  import tempfile
  from io_in_out import io_hash_fullpath
  import errno
  import stat

  with open_remote(hosts[0]) as sftp_from:
    with open_remote(hosts[1]) as sftp_to:
      for file_from,file_to in files:
        # test exists
        try:
          sftp_from.lstat(file_from)
        except IOError as er:
          print('[!] error {} {}'.format(er,file_from))
          continue

        tmpf = tempfile.mkstemp('_ssh')
        os.close(tmpf[0])
        tmpf = tmpf[1]
        sftp_from.get(file_from,tmpf)
        m = io_hash_fullpath(tmpf)
        print('[+] get {} to {} md5={}'.format(file_from,tmpf,m))

        # sftp_to.open(t)
        # sftp_to.lstat(t)
        # both return Errno 2 No such file

        # if exists, remove it
        try:
          sftp_to.lstat(file_to)
          sftp_to.remove(file_to)
        except IOError as er:
          if not (er.errno == errno.ENOENT):
            raise  er
        sftp_to.put(tmpf,file_to)

        print('[+] put to {rh}:{rp}'.format(rh=hosts[1],rp=file_to))

        # add execute mode
        with open(tmpf) as fr_tmp:
          header = fr_tmp.read(4)
          if header[1::] == 'ELF':
            st = sftp_to.lstat(file_to)
            sftp_to.chmod(file_to,st.st_mode |stat.S_IEXEC)

        print('')
        os.remove(tmpf)
