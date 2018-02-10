# coding=utf-8

'''
 the file shows ipaddress convert

 ipaddress is a Python 3.3+ package


  The "n" stands for "network", and "p" for "presentation". Or "text presentation". But you can think of it as "printable". "ntop" is "network to printable". See?
  https://www.zhihu.com/question/26013523/answer/31817088

  *ntohl 'n' means network, 'h' means host

  p = u"192.0.2.1"
  v1 = socket.inet_aton(p) # '\xc0\x00\x02\x01'
  v2 = hex_out(v1) #  ['0xc0', '0x0', '0x2', '0x1']
  v3 = v1.encode('hex') # 'c0000201'
  v4 = int(v3,16) # 3221225985

'''

import os
import sys

import unittest
import socket
import struct

def hex_out(v):
  '''
  hex(e)  is  32 -> 0x20
  '''
  return [hex(ord(e)) for e in v]

def ipaddress_pton(arg):
  pvs = arg.split('.')
  pvs = [int(v,10) for v in pvs]
  r = 0
  for i,pv in enumerate(pvs):
    r = r + (pv<<(i*8))
  return r


def ipaddress_ptoh(arg):
  pvs = arg.split('.')
  pvs = [int(v, 10) for v in pvs]
  r = 0
  pvs.reverse() # reverse at self
  for i,pv in enumerate(pvs):
    r = r + (pv<<(i*8))
  return  r

def ipaddress_ntop(arg):
  r = []
  for i in range(4):
    v = (arg >> (i * 8)) & 0xFF
    r.append('{0}'.format(v))
  return '.'.join(r)

def ipaddress_htop(arg):
    v = socket.htonl(arg)
    return ipaddress_ntop(v)


def ipaddress_pton2(p):
  v1 = socket.inet_aton(p)
  return struct.unpack('<I',v1)[0]

def ipaddress_ptoh2(p):
  v1 = socket.inet_aton(p)
  return struct.unpack('>I',v1)[0]
  # 虽然 `>` 是网络序，但 v1 就是网络序,因此会反向


def ipaddress_ntop2(n):
  v = struct.pack('<I',n)
  return socket.inet_ntoa(v)

def ipaddress_htop2(h):
  v = struct.pack('>I',h)
  return socket.inet_ntoa(v)

def ipaddress_ptoh3(p):
  v1 = socket.inet_aton(p)
  v2 = v1.encode('hex')
  return int(v2,16)

def ipaddress_htop3(arg):
  v = hex(arg)[2::]
  v = v.rstrip('L')
  return socket.inet_ntoa(v.decode('hex'))


def ipaddress_pton_unix(arg):
  '''
  inet_pton is only for unix
  '''
  return int(socket.inet_pton(socket.AF_INET,arg).encode('hex'),16)


g_data = [
  # printable        network order     host order
  (u'127.0.0.1',16777343 ,2130706433),
(u'192.145.109.100',1684902336 ,3230756196),
(u'192.168.1.3',50440384 ,3232235779),
(u'192.168.0.1',16820416 ,3232235521),
(u'192.168.34.12',203598016 ,3232244236),
              #10200C0    #C0000201
(u'192.0.2.1',16908480 ,3221225985),
]


class TestCase(unittest.TestCase):
  def test1(self):

    for arg in g_data:
      n1 = ipaddress_pton(arg[0])
      self.assertEqual(n1,arg[1])
      p = ipaddress_ntop(n1)
      self.assertEqual(p,arg[0])

    for arg in g_data:
      h1 = ipaddress_ptoh(arg[0])
      self.assertEqual(h1, arg[2])

      p = ipaddress_htop(h1)
      self.assertEqual(p,arg[0])

    for arg in g_data:
      n = ipaddress_pton2(arg[0])
      self.assertEqual(n,arg[1])
      p = ipaddress_ntop2(n)
      self.assertEqual(p,arg[0])

    for arg in g_data:
      h = ipaddress_ptoh2(arg[0])
      self.assertEqual(h,arg[2])
      p=  ipaddress_htop2(h)
      self.assertEqual(p,arg[0])

    for arg in g_data:
      h = ipaddress_ptoh3(arg[0])
      self.assertEqual(h,arg[2])

def entry():
  import ipaddress
  i = u'127.0.0.1'
  a = ipaddress.ip_address(i)

  import pdb
  pdb.set_trace()

  print(int(a))
  print(str(a))

  v = 3221225473
  print socket.ntohl(v)

def format_data():
  import ipaddress
  for arg in g_data:
    h = int(ipaddress.ip_address(arg[0]))
    print("(u'{}',{} ,{}),".format(arg[0],socket.htonl(h),h))

def entry2():
  p = u"192.0.2.1"
  v1 = socket.inet_aton(p) # '\xc0\x00\x02\x01'
  v2 = hex_out(v1) #  ['0xc0', '0x0', '0x2', '0x1']
  v3 = v1.encode('hex') # 'c0000201'
  v4 = int(v3,16) # 3221225985
  v5 = struct.unpack('<I',v1)[0] #16908480
  v6 = struct.unpack('>I',v1)[0] # 3221225985
  v7 = struct.unpack('I',v1)[0] #16908480
  print(v1,v2,v3,v4,v5,v6,v7)

if __name__ == '__main__':
  unittest.main()
  #entry2()
