# coding=utf-8

# bit fields in python http://varx.org/wordpress/2016/02/03/bit-fields-in-python/
# [Black Hat Python: Building a UDP Scanner] http://bt3gl.github.io/black-hat-python-building-a-udp-scanner.html
# [python official doc]https://docs.python.org/2/library/struct.html
# [Raw socket programming in python (Linux)] http://www.binarytides.com/raw-socket-programming-in-python-linux/
# [浅谈拒绝服务攻击的原理与防御（7）：用Python和C实现syn flood攻击] http://www.freebuf.com/articles/network/130357.html
# [tcp syn flood]https://gist.github.com/fffaraz/57144833c6ef8bd9d453

# 网络用到的结构字段数据用的是大端传递 python 有两种方法把数据做成大端
#   1 使用 struct.unpack 输入小端数据
#   2 使用 ctypes.BigEndianStructure 赋值后直接是大端数据

# python dpkt lib 

# ------------------------------------------------------------------------------
# CHANGELOG:
# 2018-01-23 not test struct_base.unpack()

import os
import sys
import struct
import random
import unittest

from ctypes import c_uint8
from ctypes import c_uint16
from ctypes import c_uint32

from ctypes import BigEndianStructure
from ctypes import sizeof
from socket import ntohl
from socket import ntohs
from socket import htonl
from socket import htons
from socket import IPPROTO_IP
from socket import IPPROTO_TCP

from net_ipaddress import ipaddress_pton
from net_ipaddress import ipaddress_ptoh
from binascii import hexlify
from binascii import unhexlify


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

    @classmethod
    def put(cls, **kwargs):
        '''
        如果没有给值 就用初始值 0，不是 None
        '''
        self = cls()
        self.version = kwargs.get('version', self.version)
        self.ihl = kwargs.get('ihl', self.ihl)
        self.tos = kwargs.get('tos', self.tos)
        self.len = kwargs.get('totallen', self.len)
        self.id = kwargs.get('id', self.id)
        self.flags = kwargs.get('flags', self.flags)
        self.offset = kwargs.get('offset', self.offset)
        self.ttl = kwargs.get('ttl', self.ttl)
        self.protocol = kwargs.get('protocol', self.protocol)
        self.checksum = kwargs.get('checksum', self.checksum)
        self.saddr = kwargs.get('saddr', self.saddr)
        self.daddr = kwargs.get('daddr', self.daddr)
        return self


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

    @classmethod
    def put(cls, **kwargs):
        '''
        这样写代码也可以 但是函数就会对参数不提示 pycharm IDE 不方便工作
        for e in ['source_port','dest_port','seq']:
          setattr(self,e,kwargs.get(e,self.get(e)))

        '''
        self = cls()
        self.source_port = kwargs.get('source_port', self.source_port)
        self.dest_port = kwargs.get('dest_port', self.dest_port)
        self.seq = kwargs.get('seq', self.seq)
        self.ack_seq = kwargs.get('ack_seq', self.ack_seq)
        self.doff = kwargs.get('doff', self.doff)
        self.res1 = kwargs.get('res1', self.res1)
        self.urg = kwargs.get('urg', self.urg)
        self.ack = kwargs.get('ack', self.ack)
        self.psh = kwargs.get('psh', self.psh)
        self.rst = kwargs.get('rst', self.rst)
        self.syn = kwargs.get('syn', self.syn)
        self.fin = kwargs.get('fin', self.fin)
        self.window = kwargs.get('window', self.window)
        self.checksum = kwargs.get('checksum', self.checksum)
        self.urg_pointer = kwargs.get('urg_pointer', self.urg_pointer)
        return self


class Toa(BaseSt):
    '''
    dpvs 中的结构体
    '''
    _pack_ = 1
    _fields_ = [
        ("opcode", c_uint8),
        ('opsize', c_uint8),
        ('port', c_uint16),
        ('addr', c_uint32),
    ]

    def put(self, **kwargs):
        self.opcode = kwargs.get('opcode', self.opcode)
        self.opsize = kwargs.get('opsize', self.opsize)
        self.port = kwargs.get('port', self.port)
        self.addr = kwargs.get('addr', self.addr)
        return self



class Ipv4PseudoHdr(BaseSt):
    _pack_=1
    _fields_=[
        ('srcAddr', c_uint32),
        ('dstAddr', c_uint32),
        ('rsv', c_uint8),
        ('protocol', c_uint8),
        ('protocolSize', c_uint16)
    ]


class TestCase(unittest.TestCase):
    def testIp(self):
        # 这种十六进制可以从 wireshark 里复制
        ipHdrHexStream = '4510003491e040003d06c25ec0916d65b6660518'
        ipHdr1, restHexStream= IpHdr.unpack(ipHdrHexStream)
        ipHdr2 = IpHdr.put(
            version=4,
            ihl=5,
            tos=0x10,
            id=0x91e0,
            totallen=52,
            flags=2,
            offset=0,
            ttl=61,
            protocol=IPPROTO_TCP,  # 6
            saddr=ipaddress_ptoh('192.145.109.101'),
            daddr=ipaddress_ptoh('182.102.5.24')
        )

        # first get big endian's bytes check sum
        csum = checksum(ipHdr2.pack())
        # csum 应该被存储为小端   csum 在代码里为小端 赋值给 iphdr 的大端结构体会有一次自动转化
        # 我们加上 csum 抵消这次自动转换
        print('Got csum = {} 0x{:x}'.format(csum,(csum)))
        ipHdr2.checksum = htons(csum)

        v1 = ipHdr1.pack()
        v2 = ipHdr2.pack()

        self.assertEqual(v1, v2)


    def testTcp(self):
        '''
        tcp option 是 uint8_t kind + uint8_t size + context 的结构
        当为 nop  kind=1 时 表示占位 无意义 就用 1 个字节
        '''
        tcpHdrHexStream = ('001625e0076e1e9e93f730d18010e5a0104c00000101050a93f730d093f730d1')

        # this tcp header contains tcp options
        # we give the tcp options big endian hex, because this time
        # we donnot care about it
        # 01 is the NOP
        # 01 is the NOP
        # 05 is kind
        # 0a is the kind size
        toaHexStream = ('0101050a93f730d093f730d1')
        toaBytes = unhexlify(toaHexStream)
        toa,toaRestHexStream = Toa.unpack(toaHexStream)

        # 这个 tcpHdr 包含的 toa 和 IpHdr.srcAddr Iphdr.dstAddr 都会加入计算 chksum
        tcpHdr = TcpHdr.put(
            source_port=22,
            dest_port=9696,  # big endian
            seq=0x076e1e9e,
            ack_seq=0x93f730d1,
            doff=5 + len(toaBytes) / 4,
            ack=1,
            window=58784,  # big endian
        )


        # checksum
        ipv4ChkSumHdr = Ipv4PseudoHdr()
        ipv4ChkSumHdr.srcAddr = ipaddress_ptoh('192.145.109.101')
        ipv4ChkSumHdr.dstAddr = ipaddress_ptoh('182.102.5.24')
        ipv4ChkSumHdr.protocol = IPPROTO_TCP
        ipv4ChkSumHdr.protocolSize = sizeof(tcpHdr) + len(toaBytes)

        tcpHdr1,restBytes = TcpHdr.unpack(tcpHdrHexStream)

        csum = checksum(ipv4ChkSumHdr.pack() + tcpHdr.pack() + toaBytes)
        tcpHdr.checksum = htons(csum)

        # print(v1)
        # print(v2)
        v = tcpHdr.pack() + toaBytes
        v= hexlify(v)



        self.assertEqual(tcpHdrHexStream,v)



if __name__ == '__main__':
    unittest.main()
