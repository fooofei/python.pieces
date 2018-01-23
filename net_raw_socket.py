# coding=utf-8

# bit fields in python http://varx.org/wordpress/2016/02/03/bit-fields-in-python/
# [Black Hat Python: Building a UDP Scanner] http://bt3gl.github.io/black-hat-python-building-a-udp-scanner.html
# [python official doc]https://docs.python.org/2/library/struct.html
# [Raw socket programming in python (Linux)] http://www.binarytides.com/raw-socket-programming-in-python-linux/
# [浅谈拒绝服务攻击的原理与防御（7）：用Python和C实现syn flood攻击] http://www.freebuf.com/articles/network/130357.html

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
import ctypes
from ctypes import c_uint8
from ctypes import c_uint16
from ctypes import c_uint32


def hex_out(v):
  return [ord(e) for e in v]


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


def iptoint32(ip):
  return int(socket.inet_aton(ip).encode('hex'), 16)


def int32toip(ip):
  return socket.inet_ntoa(hex(ip)[2:].decode('hex'))


class struct_base(ctypes.BigEndianStructure):
  '''
  用于定义网络相关结构体的父类结构体
  封装了几个辅助函数 方便在结构体和网络二进制数据中转换
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
    ("sum", c_uint16),

    ("saddr", c_uint32),
    ("daddr", c_uint32),
  ]

  def put(self, **kwargs):
    self.version = kwargs.get('version', self.version)
    self.ihl = kwargs.get('ihl', self.ihl)
    self.tos = kwargs.get('tos', self.tos)
    self.len = kwargs.get('totallen', self.len)
    self.id = kwargs.get('id', self.id)
    self.flags = kwargs.get('flags', self.flags)
    self.offset = kwargs.get('offset', self.offset)
    self.ttl = kwargs.get('ttl', self.ttl)
    self.protocol = kwargs.get('protocol', self.protocol)
    self.sum = kwargs.get('sum', self.sum)
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


def make(dest_host):
  source_ip = '192.168.1.101'

  # kernel will fill the correct checksum
  # kernel will fill the correct total length
  ip_hdr = IP().put(
    ihl=5,
    version=4,
    id=54321,
    ttl=255,
    protocol=socket.IPPROTO_TCP,
    saddr=iptoint32(source_ip),
    daddr=iptoint32(dest_host[0])
  )

  tcp_user_data = tcpopt_addr().put(
    opcode=254,
    opsize=8,
    port=88,
    addr=iptoint32('100.101.102.103')  # see the ip in tcp options
  )

  tcp_hdr = TCP().put(
    source_port=1234,
    dest_port=dest_host[1],
    seq=454,
    doff=5 + ctypes.sizeof(tcp_user_data) / 4,
    syn=1,
    window=socket.htons(5840)
  )

  tcp_length = len(tcp_hdr.pack()) + len(tcp_user_data.pack())

  # or
  psh = struct.pack('!IIBBH', ip_hdr.saddr, ip_hdr.daddr,
                    0, socket.IPPROTO_TCP, tcp_length
                    )
  # psh = struct.pack('!4s4sBBH',socket.inet_aton(source_ip),
  #                  socket.inet_aton(dest_ip),
  #                  0, socket.IPPROTO_TCP,tcp_length
  #                  )

  psh = psh + tcp_hdr.pack() + tcp_user_data.pack()
  tcp_check = checksum(psh)

  tcp_hdr.put(checksum=tcp_check)

  packet = ip_hdr.pack() + tcp_hdr.pack() + tcp_user_data.pack()

  return packet


def entry():
  s = socket.socket(socket.AF_INET, socket.SOCK_RAW, 6)
  s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

  count = 0
  while 1:
    count += 1
    print('[+] sendto count = {count}'.format(count=count))

    dst = ('ip1', 80)
    packet = make(dst)
    s.sendto(packet, dst)

    import pdb
    pdb.set_trace()

  s.close()


if __name__ == '__main__':
  pass
