# coding=utf-8

'''
this file shows transfer file through 3 machine.

A->B->C

B is our python script machine

'''

import os
import subprocess
from contextlib import contextmanager

def io_hash_fullpath(filename):
    pass

def solution1():
    '''
    一个示范 A B C 都是 linux 机器
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
        if ret_code !=0:
            break

    if ret_code == 0:
        for f in files:
            arg1 = os.path.join(local_path_b, f)
            arg2 = os.path.join(scp_path_c, f)
            cmds = ['scp', arg1, arg2]
            ret_code = subprocess.call(cmds)


import paramiko
import errno
import stat
import itertools
import tempfile
@contextmanager
def open_remote(host):
    '''
    paramiko 的连接
    '''

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
    A -> B -> C 中如果 B 是 Windows，而且我们在 B 中运行这个脚本

    from = A
    to = C

    这是用 paramiko 的，也有使用 fabric 的用法

    put <files_from> to <files_to>
    :param hosts:  [(ip1,port1,user1), (ip2,port2,user2)]
    :param files: [(file1_from,file1_to),(file2_from,file2_to),...]
    :return:
    '''


    with open_remote(hosts[0]) as sftp_from:
        with open_remote(hosts[1]) as sftp_to:
            for file_from, file_to in files:
                # test exists
                try:
                    sftp_from.lstat(file_from)
                except IOError as er:
                    print('[!] error {} of file {}'.format(er, file_from))
                    continue

                tmpf = tempfile.mkstemp('_ssh')
                os.close(tmpf[0])
                tmpf = tmpf[1]
                sftp_from.get(file_from, tmpf)
                m = io_hash_fullpath(tmpf)
                print('[+] get {} to {} md5={}'.format(file_from, tmpf, m))

                # sftp_to.open(t)
                # sftp_to.lstat(t)
                # both return Errno 2 No such file

                # if exists, remove it
                try:
                    sftp_to.lstat(file_to)
                    sftp_to.remove(file_to)
                except IOError as er:
                    if not (er.errno == errno.ENOENT):
                        raise er
                sftp_to.put(tmpf, file_to)

                print('[+] put to {rh}:{rp}'.format(rh=hosts[1], rp=file_to))

                # add execute mode
                with open(tmpf) as fr_tmp:
                    header = fr_tmp.read(4)
                    if header[1::] == 'ELF':
                        st = sftp_to.lstat(file_to)
                        sftp_to.chmod(file_to, st.st_mode | stat.S_IEXEC)

                print('')
                os.remove(tmpf)




from fabric import Connection as SSHConnection

@contextmanager
def connect(host):
    '''

    :param host: ("root@1.1.1.1", "password" or "", <port>)
    :return:
    '''
    cnt_kwargs = {}
    if host[1]:
        cnt_kwargs.update({"password": host[1]})
    else:
        cnt_kwargs.update({"key_filename": "<ssh key>", "look_for_keys": False,})

    cnt_kwargs.update({
        "banner_timeout":60, # prevent :SSHException: Error reading SSH protocol banner
        "compress":True,
                       })
    cnn = SSHConnection(host=host[0], port=host[2],
                        connect_kwargs=cnt_kwargs,
                        connect_timeout=60,
                        # forward_agent=True # if not, rsync always error Host key verification fail
                        )

    try:
        yield cnn
    finally:
        cnn.close()



def solution3(hosts, files):

    with connect(hosts[0]) as cnn_from:
        with connect(hosts[1]) as cnn_to:
            for file_from, file_to in files:
                # test exists
                try:
                    cnn_from.lstat(file_from)
                except IOError as er:
                    print('[!] error {} of file {}'.format(er, file_from))
                    continue

                tmpf = tempfile.mkstemp('_ssh')
                os.close(tmpf[0])
                tmpf = tmpf[1]

                try:
                    rst = cnn_from.get(remote=file_from,
                                 local = tmpf)
                    m = io_hash_fullpath(tmpf)
                    print('[+] get {} to {} md5={}'.format(file_from, tmpf, m))

                    # 不知道这个 mode 匹配在 Windows 和 Linux 之间会怎样
                    rst = cnn_to.put(local = tmpf,
                                     remote = file_to,
                                     preserve_mode=True)

                    print('[+] put to {rh}:{rp}'.format(rh=hosts[1], rp=file_to))


                except Exception as err:
                    print("err {} of {}->{}".format(err, file_from, file_to))
                finally:
                    os.remove(tmpf)
