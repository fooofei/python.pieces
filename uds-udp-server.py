#coding=utf-8


import os
import sys
import socket
import pdb

curpath = os.path.dirname(os.path.realpath(__file__))

def entry():
    name = 'uds_socket_demo'
    svaddr = os.path.join(curpath,os.path.join(curpath,name))

    if os.path.exists(svaddr):
        os.unlink(svaddr) # = os.remove
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.bind(svaddr)
    print('bind to {adr}'.format(adr=svaddr))
    data, claddr=sock.recvfrom(1024)
    if data:
        print('recv {dt} from {ad}'.format(dt=data,ad=claddr))

    i=0
    while i<1000:
        sock.sendto("hello"*110,claddr)  # 这个 send 又成了 block 的
        i+=1

    sock.sendto('end', claddr)
    sock.close()
    os.remove(svaddr)
    print('Alread sent {c} msgs'.format(c=i))

if __name__ == '__main__':
    entry()
