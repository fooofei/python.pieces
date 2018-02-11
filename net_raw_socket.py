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

# ------------------------------------------------------------------------------
# CHANGELOG:
# 2018-01-23 not test struct_base.unpack()

import os
import sys
import socket
import struct
import random
import unittest
import ctypes
from ctypes import c_uint8
from ctypes import c_uint16
from ctypes import c_uint32

from net_ipaddress import ipaddress_pton
from net_ipaddress import ipaddress_ptoh


def hex_out(v):
  '''
  hex(e)  is  32 -> 0x20
  '''
  return [hex(ord(e)) for e in v]


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


class struct_base(ctypes.BigEndianStructure):
  '''
  用于定义网络相关结构体的父类结构体
  封装了几个辅助函数 方便在结构体和网络二进制数据中转换

  这样生成的结构体 字节>1 的赋值应该用小端 主机序

  '''

  def pack(self):
    return buffer(self)[:]

  def unpack(self, bytes):
    size = min(len(bytes), ctypes.sizeof(self))
    ctypes.memmove(ctypes.addressof(self), bytes, size)

  def to_bits(self):
    c = self.pack()
    r = [bin(ord(e)) for e in c]
    return ' '.join(r)


class IP(struct_base):
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

  def put(self, **kwargs):
    '''
    如果没有给值 就用初始值 0，不是 None
    '''
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


class TCP(struct_base):
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

  def put(self, **kwargs):
    '''
    这样写代码也可以 但是函数就会对参数不提示 pycharm IDE 不方便工作
    for e in ['source_port','dest_port','seq']:
      setattr(self,e,kwargs.get(e,self.get(e)))

    '''
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


class tcpopt_addr(struct_base):
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


class TestCase(unittest.TestCase):
  def test_ip(self):
    s_ip_header = '45 10 00 34 91 e0 40 00 3d 06 c2 5e c0 91 6d 65 b6 66 05 18'
    hex_ip_header = s_2_hex(s_ip_header)

    iphdr = IP().put(
      version=4,
      ihl=5,
      tos=0x10,
      id = 0x91e0,
      totallen=52,
      flags=2,
      offset=0,
      ttl=61,
      protocol=socket.IPPROTO_TCP, # 6
      saddr=ipaddress_ptoh('192.145.109.101'),
      daddr=ipaddress_ptoh('182.102.5.24')
    )

    # first get big endian's bytes check sum
    v = iphdr.pack()
    csum = checksum(v)
    v = iphdr.put(checksum=socket.htons(csum)).pack()

    v1 = hex_out(hex_ip_header)
    v2 = hex_out(v)

    #print(v1)
    #print(v2)

    self.assertEqual(v1,v2)


  def test_tcp(self):
    '''
    tcp option 是 uint8_t kind + uint8_t size + context 的结构
    当为 nop  kind=1 时 表示占位 无意义 就用 1 个字节
    '''
    s_tcp_header = (
      '00 16 25 e0 07 6e 1e 9e 93 f7 30 d1 80 10 e5 a0 '
      '10 4c 00 00 01 01 05 0a 93 f7 30 d0 93 f7 30 d1'
    )
    # this tcp header contains tcp options
    # we give the tcp options big endian hex, because this time
    # we donnot care about it
    # 01 is the NOP
    # 01 is the NOP
    # 05 is kind
    # 0a is the kind size
    tcp_options = s_2_hex('01 01 05 0a 93 f7 30 d0 93 f7 30 d1')

    hex_tcp_header = s_2_hex(s_tcp_header)
    tcphdr = TCP().put(
      source_port=22,
      dest_port=9696, # big endian
      seq=0x076e1e9e,
      ack_seq=0x93f730d1,
      doff=5 + len(tcp_options)/4,
      ack=1,
      window=58784, # big endian
    )

    v1 = hex_out(hex_tcp_header)

    # checksum
    psh = struct.pack('>IIBBH',ipaddress_ptoh('192.145.109.101'),
                    ipaddress_ptoh('182.102.5.24'),
                    0, socket.IPPROTO_TCP,len(tcphdr.pack())+len(tcp_options)
                  )
    csum = checksum(psh + tcphdr.pack()+tcp_options)
    tcphdr.put(checksum=socket.htons(csum))
    v2 = hex_out(tcphdr.pack()+tcp_options)

    #print(v1)
    #print(v2)

    self.assertEqual(v1,v2)


def s_2_hex(s):
  ss = s.split(' ')
  h = ''.join(ss)
  return h.decode('hex')


def entry():
  pass


if __name__ == '__main__':
  unittest.main()
