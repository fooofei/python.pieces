#coding=utf-8

'''
测试事件

ncat -lvkt

ncat -vt 127.0.0.1 31337


1 测试如果对端SOCKET 强制结束，发来 FIN 报文后，
本端的 READ 事件会不会一直有，会一直有。

2 测试如果同时关注一个 fd 的读和写，会不会出来两个事件，
测试这个的目的在于，如果通过 epoll 来返回一个事件数组，
在处理这个事件数组时，处理第一个事件，发现需要做某些动作，
这个动作可能会破坏对象实例，导致在处理第二个事件时，
实例被删除掉，找不到，就会异常。

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
from select import POLLOUT


class Poller(object):
    '''简单封装 select.poll 外部注册 fd 和回调，事件到达后自动调用'''
    def __init__(self):
        self._p = select.poll()
        self._callbacks = {}

    def register(self, fd, events, callback, *args):
        self._p.register(fd, events)
        self._callbacks[fd.fileno()]=(callback, fd, args)

    def run_io_loop(self, loop_max_cnt=1000):
        cnt = 0
        while cnt < loop_max_cnt:
            cnt += 1
            r = self._p.poll(-1)
            for fn,revents in r:
                value = self._callbacks[fn]
                value[0](value[1],revents, *value[2])

def listen_socket_event_callback(fd, revents, laddr, pl):
    '''listen 的回调函数，生成一个 client socket '''
    print("listen_socket_event_callback-> {},{},{}"
          .format(fd, revents, laddr))
    clt_socket, raddr = fd.accept()
    print("accept {}/{}".format(raddr, laddr))
    clt_socket.setblocking(False)
    pl.register(clt_socket, POLLIN | POLLHUP | POLLOUT, clt_socket_event_callback)

def clt_socket_event_callback(fd, revents):
    '''client socket 的回调函数'''
    print("clt_socket_event_callback-> {},{}".format(fd, event_string(revents)))
    if revents & POLLIN:
        rx = fd.recv(128 * 1024)
        print("clt_socket_event_callback->rx[len={},{}]".format(len(rx),rx))
    if revents & POLLHUP:
        pass


def event_string(ev):
    '''把events int 转化为 human-readable '''
    vars = [
        (0x01, "EPOLLIN"),
        (0x02, "EPOLLPRI"),
        (0x04, "EPOLLOUT"),
        (0x08, "EPOLLERR"),
        (0x10, "EPOLLHUP"),

        (0x40, "EPOLLRDNORM"),
        (0x80, "EPOLLRDBAND"),
        (0x100, "EPOLLWRNORM"),
        (0x200, "EPOLLWRBAND"),
        (0x400, "EPOLLMSG"),

        (0x2000, "EPOLLRDHUP"),
    ]
    if isinstance(ev, str) and ev.startswith("0x"):
        ev = int(ev, 16)
    else:
        ev = int(ev)
    r = []
    for var in vars:
        if (var[0] & ev):
            r.append(var[1])
    return " ".join(r)

def entry():
    laddr = ("127.0.0.1", 4456)
    listen_socket = socket(AF_INET, SOCK_STREAM)
    listen_socket.setblocking(False)
    listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    listen_socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)

    listen_socket.bind(laddr)
    listen_socket.listen(3)

    print("listen on {}".format(laddr))

    pl = Poller()

    pl.register(listen_socket, POLLIN, listen_socket_event_callback, laddr, pl)

    pl.run_io_loop(loop_max_cnt=10)

if __name__ == '__main__':
    entry()