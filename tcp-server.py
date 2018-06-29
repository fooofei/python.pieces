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

'''

import os
import sys
import SocketServer
import binascii
import socket

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
    sfd.bind(addr)
    sfd.listen(5)
    print('[+] bind to {}'.format(addr))
    while True:
        cfd,addr = sfd.accept()

        while True:
            data = cfd.recv(1024)
            print(binascii.hexlify(data))

if __name__ == '__main__':
    entry()
