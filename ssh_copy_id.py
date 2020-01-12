#coding=utf-8
'''
python3
先用 password 模式 ssh 登陆主机，然后把自己的 ssh key 加入到机器中
'''

import os
import sys
from fabric import Connection as SSHConnection
from socket import inet_pton
from socket import ntohl
from socket import inet_ntop
from socket import htonl
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOCK_DGRAM
from socket import SHUT_WR
from struct import unpack
from socket import socket
from struct import pack
from pprint import pformat
from invoke import Responder
from paramiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
from contextlib import contextmanager
from socket import timeout as sotimeout
from socket import error as soerror
from fabric import transfer
from fabric import Result as SSHRunResult
from json import dumps as jdumps
from json import loads as jloads
from datetime import datetime as DateTime
from binascii import hexlify
from timeit import default_timer as Time


def ssh_run(cnn, cmd):
    for i in range(2, 10):
        try:
            return cnn.run(**{"command": cmd, "hide": True, "warn": True, "encoding": "utf-8"})
        except EOFError as eoferr:
            # INFO:paramiko.transport:Connected (version 2.0, client OpenSSH_7.4)
            # DEBUG:paramiko.transport:EOF in transport thread
            print(f"try {cmd} at {cnn.original_host} {i} times {eoferr}")
            sys.stdout.flush()


def view_resp(rc):
    if isinstance(rc, transfer.Result):
        return f"put to {rc.remote}"
    if isinstance(rc, SSHRunResult):
        return f"{rc.command} \n  return_code={rc.return_code}\n  stderr=\n{rc.stderr}\n  stdout=\n{rc.stdout}"
    return f"{rc}"


@contextmanager
def connect(host_info):
    '''
    :param host_info:
        {"password": <optional>,
        "host": "ip addr",
        "port": int, <optional>,
        "user": <optional>,
        }
    :return:
    '''
    cnt_kwargs = {}
    passwd = host_info.get("password", "")
    if passwd != "":
        cnt_kwargs.update({"password": passwd})
    else:
        cnt_kwargs.update({"key_filename": "<>", "look_for_keys": False, })

    cnt_kwargs.update({
        "banner_timeout": 60,  # prevent :SSHException: Error reading SSH protocol banner
        "compress": True,
    })
    cnn = SSHConnection(host=host_info.get("host"),
                        port=host_info.get("port", 22),
                        user=host_info.get("user", "root"),
                        connect_kwargs=cnt_kwargs,
                        connect_timeout=60,
                        # forward_agent=True # if not, rsync always error Host key verification fail
                        )

    try:
        yield cnn
    finally:
        cnn.close()


def setup_ssh_key(cnn):
    '''
    ssh-keygen -t ed25519
    '''
    key0 = ("<>")

    rc = ssh_run(cnn, "mkdir -p ~/.ssh")
    print(view_resp(rc))
    rc = ssh_run(cnn, '''printf "\n{}" >> ~/.ssh/authorized_keys'''.format(key0))
    print(view_resp(rc))


    # remove duplicate
    with cnn.prefix("cd ~/.ssh"):
        ssh_run(cnn, "rm -f bak")
        ssh_run(cnn, "cat authorized_keys | sort | uniq > bak")
        ssh_run(cnn, "mv -f bak authorized_keys")
def main():

    onlines = []
    offlines = []
    try:
        hosts = [
        ]

        for i, host in enumerate(hosts):
            print(f"-[{i}]--------------- {host}")
            sys.stdout.flush()

            for _ in range(2):

                try:
                    with connect(host) as cnn:

                        setup_ssh_key(cnn)

                        sys.stdout.flush()
                        onlines.append(host)
                        break
                except SSHException as ssherr:
                    print(f"{type(ssherr)} {ssherr}")
                    continue
                except sotimeout as tmoerr:
                    print(f"{type(tmoerr)} {tmoerr}")
                    continue
                except soerror as soerr:
                    print(f"{type(soerr)} {soerr}")
                    continue
            else:
                offlines.append(host)
    except KeyboardInterrupt:
        pass

    print('Onlines=[')
    for h in onlines:
        print(f'''"{host_line(h)}",''')
    print("]")
    print('Offlines=[')
    for h in offlines:
        print(f'''"{host_line(h)}",''')
    print("]")


if __name__ == '__main__':
    main()
