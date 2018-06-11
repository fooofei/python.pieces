#coding=utf-8

import os
import sys

import socket

def entry():
    addr = ('127.0.0.1',6666)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(addr)
    print('bind to {adr}'.format(adr=addr))
    data, rvaddr=sock.recvfrom(1024)

    if data:
        print('recv {dt}'.format(dt=data))

    i=0
    while i<1000:
        sock.sendto("hello"*110, rvaddr)
        i+=1

    sock.sendto('end',rvaddr)
    print('Alread sent {c} msgs'.format(c=i))

if __name__ == '__main__':
    entry()
