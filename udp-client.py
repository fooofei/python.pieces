#coding=utf-8
'''
我不做其他额外的配置 linux 丢包概率特别大 5 次 就1 次成功 ， Windows 没有失败的

使用 setsockopt RCVBUF 之后 linux 上的丢包就少了 不行，丢包还是不能忍受

IPC 通讯使用 UDP 讨论 https://stackoverflow.com/questions/39338588/is-udp-a-reliable-protocol-for-ipc

结论： 还是老老实实用 TCP 吧

用 TCP 的编程模型是 先有一个 UDP socket 用来接收命令的 接收到要发送大数据的命令
  这时候能拿到 client 连接的地址也就是端口 然后开启 TCP socket 发送数据

新的想法是使用 Unix Domain Socket


测试 send 一侧探测对方端口不在了
1 send 一侧 不管 recv 一侧在不在 都能send，返回值都是正确的
2 recv 一侧 在send一侧，端口bind后，发送数据前，recv MSG_DONTWAIT 错误为
    socket.error: [Errno 35] Resource temporarily unavailable
  在 send一侧关闭时，recv 一样的错误，没有办法感知对方端口是否存在

如果 udp recvfrom 传递空间大小不够会有错误 errno = 10040

'''

import socket

def entry():

    addr = ('127.0.0.1',6666)
    cfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cfd.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,20*1024*1024)

    cfd.sendto('you can send msg', addr)
    c = 0
    while True:
        try:
            data,addr = cfd.recvfrom(10)
            # UDP 无顺序 不能这样做结束判定
            #if data=='end':
            #    break
            print('[{c}] {dt}'.format(c=c,dt=data))
            c += 1

            if c % 1000 ==0:
                print('rcv {}'.format(c))

        except KeyboardInterrupt:
            break
    print('recv {c} msgs'.format(c=c))

if __name__ == '__main__':
    entry()
