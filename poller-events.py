#coding=utf-8

'''
测试事件

ncat -lvkt

ncat -vt 127.0.0.1 31337


1 测试如果对端SOCKET 强制结束，发来 FIN 报文后，
本端的 READ 事件会不会一直有，会一直有。

'''

import os
import sys
import select

from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SO_REUSEADDR
from socket import SOL_SOCKET
from socket import SO_REUSEPORT
from select import POLLIN
from select import POLLERR
from select import POLLHUP


class Poller(object):
    def __init__(self):
        self._p = select.poll()
        self._callbacks = {}

    def register(self, fd, events, callback, *args):
        self._p.register(fd, events)
        self._callbacks[fd.fileno()]=(callback, fd, args)

    def run_io_loop(self, max_loop_cnt=1000):
        cnt = 0
        while cnt < max_loop_cnt:
            cnt += 1
            r = self._p.poll(-1)
            for fn,revents in r:
                value = self._callbacks[fn]
                value[0](value[1],revents, *value[2])

def listen_socket_event_callback(fd, revents, laddr, pl):
    print("listen_socket_event_callback-> {},{},{}"
          .format(fd, revents, laddr))
    clt_socket, raddr = fd.accept()
    print("accept {}/{}".format(raddr, laddr))
    clt_socket.setblocking(False)
    pl.register(clt_socket, POLLIN | POLLHUP, clt_socket_event_callback)

def clt_socket_event_callback(fd, revents):
    print("clt_socket_event_callback-> {},{}".format(fd, revents))
    if revents & POLLIN:
        rx = fd.recv(128 * 1024)
        print("clt_socket_event_callback->rx[len={},{}]".format(len(rx),rx))
    if revents & POLLHUP:
        pass

def entry():
    laddr = ("127.0.0.1", 4456)
    listen_socket = socket(AF_INET, SOCK_STREAM)
    listen_socket.setblocking(False)
    listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    listen_socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)

    listen_socket.bind(laddr)
    listen_socket.listen(3)


    pl = Poller()

    pl.register(listen_socket, POLLIN, listen_socket_event_callback, laddr, pl)

    pl.run_io_loop(max_loop_cnt=10)

if __name__ == '__main__':
    entry()