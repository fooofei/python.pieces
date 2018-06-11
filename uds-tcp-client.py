#coding=utf-8

'''
能全部接收到 但因为是字节流式的数据发送接收
发送 1000 此，并不是接收到 1000 次，

'''

import os
import sys
import socket
import pdb

curpath = os.path.dirname(os.path.realpath(__file__))

def entry():
    svaddr = os.path.join(curpath,os.path.join(curpath,'uds_socket_demo'))
    # 没有 claddr 也可以 
    claddr = os.path.join(curpath, os.path.join(curpath,'uds_socket_demo_client'))
    if os.path.exists(claddr):
        os.remove(claddr)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(claddr)
    sock.connect(svaddr)

    c = 0
    while True:
        try:
            data = sock.recv(1024)
            if data=='end':
                break
            if not data:  # 为什么一直有数据呢  这个流式的 TCP 不能用
                break
            print('[{c}] {dt}'.format(c=c,dt=data))
            c += 1
        except KeyboardInterrupt:
            break
    sock.close()
    os.remove(claddr)
    print('recv {c} msgs'.format(c=c))


if __name__ == '__main__':
    entry()
