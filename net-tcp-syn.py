# coding=utf-8


import os
import sys

from ctypes import BigEndianStructure
from ctypes import sizeof
from ctypes import c_uint8
from ctypes import c_uint16
from ctypes import c_uint32

from socket import IPPROTO_TCP
from socket import ntohl
from socket import htonl
from socket import htons
from socket import ntohs
from binascii import hexlify
from binascii import unhexlify
from random import randint
from itertools import count
from timeit import default_timer
from threading import Thread
import signal
import time
from concurrent.futures import ThreadPoolExecutor

def ipaddress_pton(arg):
    pvs = arg.split('.')
    pvs = [int(v, 10) for v in pvs]
    r = 0
    for i, pv in enumerate(pvs):
        r = r + (pv << (i * 8))
    return r

def ipaddress_ptoh(arg):
    pvs = arg.split('.')
    pvs = [int(v, 10) for v in pvs]
    r = 0
    pvs.reverse()  # reverse at self
    for i, pv in enumerate(pvs):
        r = r + (pv << (i * 8))
    return r

def checksum(data):
    s = 0
    n = len(data) % 2
    for i in range(0, len(data) - n, 2):
        s += ord(data[i]) + (ord(data[i + 1]) << 8)
    if n:
        s += ord(data[i + 1])
    while (s >> 16):
        s = (s & 0xFFFF) + (s >> 16)
    s = ~s & 0xffff
    return s


class BaseSt(BigEndianStructure):
    '''
        用于定义网络相关结构体的父类结构体
        封装了几个辅助函数 方便在结构体和网络二进制数据中转换
        这样生成的结构体 字节>1 的赋值应该用小端 主机序 因为我们在代码里写的都是小端
    '''

    def pack(self):
        return buffer(self)[:]

    @classmethod
    def unpack(cls, hexStream):
        a = unhexlify(hexStream)
        b = cls.from_buffer_copy(a)
        restBytes = a[sizeof(b)::]
        return b, hexlify(restBytes)


class IpHdr(BaseSt):
    _pack_ = 1
    _fields_ = [
        ("version", c_uint8, 4),
        ("ihl", c_uint8, 4),  # length
        ("tos", c_uint8),  # type of service
        ("len", c_uint16),  # total length

        ("id", c_uint16),
        ("flags", c_uint16, 3),
        ("offset", c_uint16, 13),  # fragment offset

        ("ttl", c_uint8),
        ("protocol", c_uint8),
        ("checksum", c_uint16),

        ("saddr", c_uint32),

        ("daddr", c_uint32),
    ]


class TcpHdr(BaseSt):
    '''
    input buffer
    output struct instance
        tcp_hdr = TCP(buffer)
    '''
    _pack_ = 1
    _fields_ = [
        ("source_port", c_uint16),
        ('dest_port', c_uint16),

        ('seq', c_uint32),
        ('ack_seq', c_uint32),

        ('doff', c_uint16, 4),
        ('res1', c_uint16, 6),
        ('urg', c_uint16, 1),
        ('ack', c_uint16, 1),
        ('psh', c_uint16, 1),
        ('rst', c_uint16, 1),
        ('syn', c_uint16, 1),
        ('fin', c_uint16, 1),
        ('window', c_uint16),

        ('checksum', c_uint16),
        ('urg_pointer', c_uint16),
    ]


class Ipv4PseudoHdr(BaseSt):
    _pack_ = 1
    _fields_ = [
        ('srcAddr', c_uint32),
        ('dstAddr', c_uint32),
        ('rsv', c_uint8),
        ('protocol', c_uint8),
        ('protocolSize', c_uint16)
    ]


def sndRawPkt1(pkts, stat):
    ''' send ip pkt from raw socket '''
    from socket import socket
    from socket import AF_INET
    from socket import SOCK_RAW
    from socket import IPPROTO_RAW
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)

    for pkt,dst in pkts:
        sockfd.sendto(pkt,0, dst)
        next(stat.cnt)
    sockfd.close()

def sndRawPktWinpcap(pkts, stat):
    ''' send ip pkt from winpcap '''
    from winpcapy import WinPcap

    # h00437043
    deviceName = '\Device\NPF_{30C74C23-86FC-4E07-8840-47716B0171E6}'
    #ifName = u'TAP-Windows Adapter V9 #5'
    ethHdr = ('e468a383202500ff30c74c230800')

    deviceName = '\Device\NPF_{C977F8A1-11E7-4C68-8D34-F9B95F1AA889}'
    ethHdr = ('04f9388aae7b3cd92b5cd1da0800')

    deviceName ='\Device\NPF_{AA85E603-D518-447B-9271-A442FF5133D6}'
    ethHdr = ('00E04C97606C001B21C1BD760800')


    ethHdr = unhexlify(ethHdr)

    with WinPcap(deviceName) as wp:
        for pkt,_ in pkts:
            wp.send(ethHdr + pkt)
            next(stat.cnt)


def makeIpPkt():
    pktHexStream = ('45000034525e400080060c530ab160b90a8126'
                    '281c781ba82456a1e3000000008002ffffd4aa0000020405b40103030101010402')
    # tcp options is '020405b40103030101010402'
    dstIp = "4.1.88.46"
    dstIp = "4.1.94.32"
    dstIp = '200.0.0.30'
    ddstPort = 80
    ipHdr, otherHexStream = IpHdr.unpack(pktHexStream)
    ipHdr.saddr = randint(1, 0xFFFFFFFF)
    ipHdr.daddr = ipaddress_ptoh(dstIp)
    tcpHdr, otherHexStream = TcpHdr.unpack(otherHexStream)
    tcpHdr.dest_port = ddstPort
    tcpHdr.source_port = randint(1, 0xFFFF)
    tcpHdr.checksum = 0
    tcpHdr.seq = randint(1, 0xFFFFFFFF)
    otherBytes = unhexlify(otherHexStream)
    ipPseudoHdr = Ipv4PseudoHdr()
    ipPseudoHdr.srcAddr = ipHdr.saddr
    ipPseudoHdr.dstAddr = ipHdr.daddr
    ipPseudoHdr.protocol = IPPROTO_TCP
    ipPseudoHdr.protocolSize = sizeof(tcpHdr) + len(otherBytes)

    csum = checksum(ipPseudoHdr.pack() + tcpHdr.pack() + otherBytes)
    tcpHdr.checksum = htons(csum)
    addr = (dstIp, 0)

    sndBuf = ipHdr.pack() + tcpHdr.pack() + otherBytes
    return sndBuf, addr

def makePktsIter():
    '''
    可以使用 rawsocket 发送 也能使用 winpcap 发送
    '''
    while True:
        v = makeIpPkt()
        yield v


class WithCurrent(object):
    def __init__(self, generator):
        self.__gen = iter(generator)
        self.current = None

    def __iter__(self):
        return self

    def n_next(self):
        self.current = next(self.__gen)
        return self.current

    def __next__(self):
        return self.n_next()

    def next(self):
        return self.n_next()

    def __call__(self):
        return self


def _func_mon(stat):
    start = default_timer()
    lastCnt = 0
    lastTime=default_timer()
    while not stat.stop:
        time.sleep(2)

        now = default_timer()
        total = 0 if stat.cnt.current is None else stat.cnt.current
        totalElapse = now-start
        totalElapse = int(totalElapse)
        v1 = '{}s total={} {}/{}=pps={}'.format(totalElapse, total,total,totalElapse,total/totalElapse if totalElapse>0 else 0)
        cur = total-lastCnt
        curElapse = now-lastTime
        curElapse = int(curElapse)
        v2 = 'current={} cpps={}'.format(cur, cur / curElapse if curElapse > 0 else 0)

        lastCnt = total
        lastTime = now
        print('{} {}'.format(v1,v2))

class Stat(object):
    def __init__(self):
        self.cnt = WithCurrent(count())
        self.stop = False

def __signal_handler(n, a):
    print('rcv {} {} we exit'.format(n,a))
    sys.exit(0)

def _func_threadpoll(args):
    arg,fun = args
    fun(*arg)

def tcpSynServeForever():
    '''
    单线程 3kpps 速度
    '''
    stat = Stat()
    concurrent = 16

    month = Thread(target=_func_mon, args=(stat,))
    month.daemon = True
    month.start()

    # 接管 CTRL+C 异常
    signal.signal(signal.SIGINT, __signal_handler)
    signal.signal(signal.SIGTERM, __signal_handler)

    try:
        tasks = []
        for _ in range(concurrent):
            tasks.append([(makePktsIter(),stat), sndRawPktWinpcap])

        with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
            r = pool.map(_func_threadpoll, tasks)
            pool.shutdown(wait=True)
            # shutdown 可能不阻塞
            list(r)

        #arg,fun = tasks[0]
        #fun(*arg)
    except Exception as er:
        raise er
    finally:
        stat.stop = True
        month.join()
        print('exit success')

#################################################################
### tests
def testTcpSyn():
    ''' 可以测试单个报文的发送 '''
    i = makeIpPkt()
    sndRawPktWinpcap([i], Stat())

def test_raw_socket():
    import socket
    #sockfd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    sndBuf = unhexlify(
        '4500003c000040003f0683610401582a0401582f005099de9cb36e3aa39d7'
        '9dea0127120c8f20000020405b40402080ab4274946030a927101030307')
    dstIp = "4.1.88.47"
    addr = (dstIp, 0)
    r = sockfd.sendto(sndBuf, addr)
    print('sndto {} size={} return={}'.format(addr, len(sndBuf), r))
    print(hexlify(sndBuf))


def deviceList():
    import winpcapy
    a = winpcapy.WinPcapDevices.list_devices()
    for k,v in a.items():
        print('{} {}'.format(k,v))


if __name__ == '__main__':
    tcpSynServeForever()
