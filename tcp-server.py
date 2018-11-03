#coding=utf-8

'''

tcp client 在 send 时如何知道 server 不可用？

    做 TCP socket client 时， 如果 server 关闭连接（recv端），client send 接收到 SIGPIPE 信号，
    会结束进程， 在send 时使用 flags=MSG_NOSIGNAL 把这个错误通过返回值来解决（返回-1， errno=EPIPE）
    特别注意，当 connect 成功，client 没有主动去探测 server时，直接send，第一次是调用返回成功，第二次是返回失败
    会损失一次数据，见这里 https://stackoverflow.com/questions/12299549/tcp-socket-detect-if-peer-has-shut-down-before-sending-linux
    查资料找到了 SO_KEEPALIVE https://notes.shichao.io/unp/ch7/ 选项可能符合我们的需要，但是发现也不符合，这个选项的心跳不可靠。
    见 https://blog.csdn.net/ctthuangcheng/article/details/8596818
    对于我们100k pps send 的场景，心跳并不及时

    python 不是通过 errno 处理的，会有异常 socket.error: [Errno 32] Broken pipe
    c 语言 是 send() != sendsize, errno == EPIPE

tcp server 在 recv 时如何知道 client 不可用？

  python 中 tcp server 如何知道 client 不在了？ server recv 返回 '' 表示 client 不在了
  c recv(sock, &buf, 1, MSG_PEEK | MSG_DONTWAIT) ==0  

  no-block socket（例如给fd设置no-block 或者 recv( MSG_DONTWAIT)）,如果 rc=-1, errno = EAGAIN ||EWOULDBLOCK
  可以说明 socket 数据当前可被取用的数据已经被取用完毕。
tcp socket file descriptor 重用
    在 socket 不可用时，想重用 socket file descriptor 为了 avoid Too many files open 错误

    我尝试了
        value = 1;
        setsockopt(s->sockfd, SOL_SOCKET, SO_REUSEPORT, &value, sizeof(value));
        setsockopt(s->sockfd, SOL_SOCKET, SO_REUSEADDR, &value, sizeof(value));
        setsockopt(s->sockfd, SOL_SOCKET, SO_LINGER, &value, sizeof(value));

    在知道 socket 无法发送数据的时候， shutdown(sockfd, SHUT_RDWR);
    然后继续 connect 也会失败，错误 #define EISCONN     106 /* Transport endpoint is already connected */

    这条路行不通

    测试发现循环 创建socket close socket ，使用的是同一个文件描述符，fd相等，不会因为打开文件过多无法创建socket

close socket 讨论
  TCP RST: Calling close() on a socket with data in the receive queue
  http://cs.baylor.edu/~donahoo/practical/CSockets/TCPRST.pdf

tcp socket 是 stream-oriented,  就是需要自己处理消息边界.
那 TLS on TCP 是 stream-oriented 还是 message-oriented 的呢？
TLS 存在 record 是解决这个问题的

一个 socket fd 设置为 no-block 的几种方式

1 socket() 创建句柄附带参数 SOCK_NONBLOCK   
  或者 accept4() 附带这个参数
  
2 存在 socketfd （句柄）之后，使用 
   int flags = fcntl(fd, F_GETFL, 0);
   fcntl(fd, F_SETFL, flags | O_NONBLOCK);
   另一种非posix标准的调用是
   ioctl(sockfd, FIONBIO, &noBlockOn=TRUE)

3 send recv 附带标记 MSG_DONTWAIT
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
