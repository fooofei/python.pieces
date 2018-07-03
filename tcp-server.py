#coding=utf-8

'''

做 TCP socket client 时， 如果 server 关闭连接，client 接收到 SIGPIPE 信号，
会结束进程， 在send 时使用 flags=MSG_NOSIGNAL 把这个错误通过返回值来解决

这时候还想重用 socket file descriptor 为了 avoid Too many files open 错误

我尝试了
    value = 1;
    setsockopt(s->sockfd, SOL_SOCKET, SO_REUSEPORT, &value, sizeof(value));
    setsockopt(s->sockfd, SOL_SOCKET, SO_REUSEADDR, &value, sizeof(value));
    setsockopt(s->sockfd, SOL_SOCKET, SO_LINGER, &value, sizeof(value));

在知道 socket 无法发送数据的时候， shutdown(sockfd, SHUT_RDWR);
然后继续 connect 也会失败，错误 #define EISCONN     106 /* Transport endpoint is already connected */

这条路行不通

测试发现循环 创建socket close socket ，使用的是同一个文件描述符，fd相等，不会因为打开文件过多无法创建socket


tcp server 如何知道 client 不在了？ server recv 返回 '' 表示 client 不在了

tcp client 怎么知道 server 不在了？ client send 收到 SIGPIPE 消息，但是 send 会带标记忽略这个消息
所以当 send 出错 我就选择不信任这个会话连接了


'''

import os
import sys
import SocketServer
import binascii
import socket
import ctypes
import json

def hexlify(value):
    return (format(v,'02x') for v in value)

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        data = self.request.recv(1024)
        print(binascii.hexlify(data))


def entry1():
    host = ('localhost',44444)

    # 这个的缺点是不方便查看 TCP stream 流是怎么接收的
    # 在使用的时候总觉得少了点数据 但是有不知道怎么找
    svr = SocketServer.TCPServer(host, MyTCPHandler)

    print('[+] bind to {}'.format(host))
    svr.serve_forever()

def entry():
    addr = ('0.0.0.0', 44444)
    sfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # socket.error: [Errno 22] Invalid argument
    #sfd.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, 1)
    sfd.bind(addr)
    sfd.listen(5)
    print('[+] bind to {}'.format(addr))

    while True:
        cfd,caddr = sfd.accept()
        print('[+] accept from {}'.format(caddr))

        while True:
            # 当 client 关闭 socket 时 这里就一直受信
            # https://docs.python.org/2/howto/sockets.html
            # 这里说 recv 返回 0 bytes 的时候，就是对方 close 的时候
            # when a recv returns 0 bytes, it means the other side has closed
            # (or is in the process of closing) the connection.
            # You will not receive any more data on this connection.
            # Ever. You may be able to send data successfully; I’ll talk more about this later.
            data = cfd.recv(1024)
            if b''== data:
                print('[!] client {} is broken'.format(caddr))
                break
            print('recv length={} {}'.format(len(data),data))



if __name__ == '__main__':
    entry()
