#coding=utf-8

'''
拥有一个 IP 报文，想发送到 IP 报文中指定的 IP 对端， 怎么做？

IP 对端是另一台机器的情况

IP 对端是本机的另一个interface 的情况


MSG_DONTROUTE 可以不用路由

socket(AF_INET, SOCK_RAW, IPPROTO_RAW /*protocol*/);
是不是需要加这个  setsockopt(iSock, IPPROTO_IP, IP_HDRINCL, (CHAR *)&uiFlag, sizeof(uiFlag));

socket(PF_PACKET, SOCK_RAW )

[C Language Examples of IPv4 and IPv6 Raw Sockets for Linux] http://www.pdbuchan.com/rawsock/rawsock.html
[A Guide to Using Raw Sockets] https://opensourceforu.com/2015/03/a-guide-to-using-raw-sockets/amp/

要解决的问题:
1 sendto 的 address 参数 如何理解， 在 socket 的 address family 为 AF_INET/PF_PACKET 时 各应该是什么

2 AF_INET PF_PACKET 区别  发现 PF_PACKET 重在接收报文上


https://github.com/AlexisTM/rawsocket_python

# how to detect SOCK_RAW support or not
    # https://docs.microsoft.com/zh-cn/windows/desktop/WinSock/tcp-ip-raw-sockets-2
    # see Limitations on Raw Sockets
Windows7 不支持RAW socket 发送 TCP， 要用winpcap，python 有 winpcapy

'''

import socket
import binascii

def send_packet_af_inet_raw(packet, dst_ip):
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    
    # 20180911 使用心得
    # IPPROTO_RAW 自己会 IP_HDRINCL=1, 如果我们继续 IP_HDRINCL=1，会导致发不出报文，还不知道原因
    #sockfd.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # IP_HDRINCL 应该是搭配IPPROTO_TCP/IPPROTO_UDP 使用
    
    # 查到资料，有以下两种方式发送ip报文
    #  sockfd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    #  sockfd.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # or
    #  sockfd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    # 在 Windows 上第一个方法报错 socket.error: [Errno 10022]  https://stackoverflow.com/questions/32590031/socket-error-errno-10022-when-using-socket-sendpacket-ip-port
    # 还不知道 sockfd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP) 是什么用法
    # 这俩都能发出报文来 Windows 发出来的报文不对，不是自己的 IP头
    # Windows 不支持 SOCK_RAW https://stackoverflow.com/questions/19029110/why-the-packets-cant-be-sent-by-raw-socket-under-windows
    
   
    # dst should be
    #memset( & sin, 0, sizeof(struct sockaddr_in));
    #sin.sin_family = AF_INET;
    #sin.sin_addr.s_addr = iphdr.ip_dst.s_addr;
    r = sockfd.sendto(packet,0,(dst_ip,0))
    print('[+] return {r}'.format(r=r))

def send_packet_pf_packet_raw(packet, dst_ip):
    ETH_P_IP = 0x0800
    # 有或者没有 ETH_P_IP 都可以
    sockfd = socket.socket(socket.PF_PACKET, socket.SOCK_RAW) #, socket.htons(ETH_P_IP)

    #sockfd.bind(('ens192', socket.htons(ETH_P_IP)))

    # 必须是 包含 ether header 的报文
    packet = '\x00\x0c\x29\x99\xef\xc3\x00\x0c\x29\x42\x48\x53\x08\x00' + packet
    assert (len(packet) == 0x62)
    # 这个有没有 bind 都能发送到
    # ETH_P_IP 或者 0 都可以
    r = sockfd.sendto(packet, ('ens192', 0)) #

    # bind 之后使用这个可以
    #r = sockfd.send(packet)
    print('[+] return {r}'.format(r=r))

def send_packet():

    # 这是一个 ICMP 的 IP 报文 我们来把它发送到目的 IP 所在的机器上
    # 你可以手动增加 eth 头，到 https://www.gasmi.net/hpd/ 网站查看这个报文的内容
    # 发送时 请用 目的侧 tcpdump 实时查看报文到达情况
    packet = ('''\x45\x00\x00\x54\x9d\x54\x40\x00\x40\x01\x1c\x37\xc0\x8c\x00\x03'''
    '''\xc0\x8c\x00\x02\x08\x00\x05\xdd\x32\xea\x00\x01\xdb\x67\x62\x5b\x00\x00'''
    '''\x00\x00\xba\xa1\x08\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17'''
    '''\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29'''
    '''\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37''')

    dst_ip = '192.140.0.2'
    assert (len(packet) == 84)

    #send_packet_af_inet_raw(packet, dst_ip)
    send_packet_pf_packet_raw(packet, dst_ip)
if __name__ == '__main__':
    send_packet()
