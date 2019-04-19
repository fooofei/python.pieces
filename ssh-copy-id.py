#coding=utf-8


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
    for i in range(2,10):
        try:
            return cnn.run(**{"command": cmd, "hide": True, "warn": True, "encoding":"utf-8"})
        except EOFError as eoferr:
            # INFO:paramiko.transport:Connected (version 2.0, client OpenSSH_7.4)
            # DEBUG:paramiko.transport:EOF in transport thread
            print("try {} at {} {} times".format(cmd, cnn.original_host, i))
            sys.stdout.flush()

def view_resp(rc):
    if isinstance(rc, transfer.Result):
        return u"put to {}".format(rc.remote).encode("utf-8")
    if isinstance(rc, SSHRunResult):
        return (u"{} \n  return_code={}\n  stderr=\n{}\n  stdout=\n{}").format(
            rc.command, rc.return_code, rc.stderr, rc.stdout).encode("utf-8")
    return u"{}".format(rc).encode("utf-8")


@contextmanager
def connect(host):
    cnt_kwargs = {}
    if host[1]:
        cnt_kwargs.update({"password": host[1]})
    else:
        cnt_kwargs.update({"key_filename": "<>", "look_for_keys": False,})

    cnt_kwargs.update({
        "banner_timeout":60, # prevent :SSHException: Error reading SSH protocol banner
        "compress":True,
                       })
    cnn = SSHConnection(host=host[0], port=22,
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

        pwd = ""
        for h in [""]:
            hosts.append(("root@{}".format(h), pwd))

        for i, host in enumerate(hosts):
            print("--------{}-------- {}".format(i, host))
            sys.stdout.flush()

            for _ in range(2):

                try:
                    with connect(host) as cnn:

                        setup_ssh_key(cnn)

                        sys.stdout.flush()
                        onlines.append(host)
                        break
                except SSHException as ssherr:
                    print("{} {}".format(type(ssherr), ssherr))
                    continue
                except sotimeout as tmoerr:
                    print("{} {}".format(type(tmoerr), tmoerr))
                    continue
                except soerror as soerr:
                    print("{} {}".format(type(soerr), soerr))
                    continue
            else:
                offlines.append(host)
    except KeyboardInterrupt:
        pass


    print('onlines=[')
    for h in onlines:
        print('''("{}",None),'''.format(h[0]))
    print("]")
    print('offlines=[')
    for h in offlines:
        print('''("{}",None),'''.format(h[0]))
    print("]")

if __name__ == '__main__':
    main()
