#coding=utf-8

'''
想了一会 对比 AF_INET UDP socket 没有显式地写 client addr, 在 UDS 中要显式地写地址

  为什么呢 其实在 AF_INET UDP socket 也是一个进程一个端口，当没显式地写地址的时候就是客户端为我们分配的地址

'''

import socket
import pdb
import os
import sys

curpath = os.path.dirname(os.path.realpath(__file__))

def entry():
    name = 'uds_socket_demo_client'
    claddr = os.path.join(curpath,os.path.join(curpath,name))

    svaddr = os.path.join(curpath, os.path.join(curpath,'uds_socket_demo'))
    if os.path.exists(claddr):
        os.unlink(claddr)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,20*1024*1024)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(claddr)
    
    # 发送这个消息的目的是为了告诉对方自己的地址 让对方给自己发消息就有地址了
    sock.sendto('you can send msg', svaddr)
    c = 0
    while True:
        try:
            data,addr = sock.recvfrom(1024)
            if data=='end':
                break
            # print('[{c}] {dt}'.format(c=c,dt=data))
            c += 1
        except KeyboardInterrupt:
            break
    sock.close()
    os.remove(claddr) # REUSE 也不行 必须清理
    print('recv {c} msgs'.format(c=c))



if __name__ == "__main__":
    entry()
