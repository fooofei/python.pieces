#coding=utf-8

import os
import sys
import threading
import socket
import timeit
from time import sleep

def basic():
    addr = ('127.0.0.1',6666)
    sfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sfd.bind(addr)
    print('bind to {adr}'.format(adr=addr))
    data, rvaddr=sfd.recvfrom(1024)

    if data:
        print('recv {dt}'.format(dt=data))

    i=0
    while i<3000:
        sfd.sendto("hello"*110, rvaddr)
        i+=1

    sfd.sendto('end',rvaddr)
    print('Alread sent {c} msgs'.format(c=i))


def _thread_func(v):
    begin = timeit.default_timer()
    while not v[0]:
        now = timeit.default_timer()
        elapse = now - begin
        elapse = int(elapse)
        if elapse>0:
            cnt = v[1]
            print('--> {}/{}={}'.format(cnt, elapse, cnt/elapse))
        sleep(2)

def entry():
    addr = ('127.0.0.1',6666)
    sfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sfd.bind(addr)
    print('bind to {adr}'.format(adr=addr))
    args = [False,0] # (stoped, count)
    th = threading.Thread(target=_thread_func, args=(args,))
    th.daemon=True
    th.start()

    data, rvaddr=sfd.recvfrom(1024)

    if data:
        print('recv {dt}'.format(dt=data))

    try:
        while True:
            sfd.sendto("hello"*110, rvaddr)
            args[1]+=1
            import pdb
            pdb.set_trace()

    except KeyboardInterrupt:
        pass
    finally:
        args[0]=True
        th.join()
        sfd.sendto('end',rvaddr)
        args[1]+=1
        print('Alread sent {c} msgs'.format(c=args[1]))



if __name__ == '__main__':
    entry()
