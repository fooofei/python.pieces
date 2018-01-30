# coding=utf-8

'''
 the file shows ipaddress convert

 ipaddress is a Python 3.3+ package


  The "n" stands for "network", and "p" for "presentation". Or "text presentation". But you can think of it as "printable". "ntop" is "network to printable". See?
  https://www.zhihu.com/question/26013523/answer/31817088

  *ntohl 'n' means network, 'h' means host

  192.0.0.1 -> 3221225473  network  big-endian -> 16777408  host little-endian

'''

import os
import sys
import ipaddress
import unittest
import socket


def ipaddress_pton(arg):
  '''
  '192.0.0.1' -> 3221225473  (network)
  '''
  pvs = arg.split('.')
  r = 0
  for pv in pvs:
    r = (r << 8) + int(pv, 10)

  return r


def ipaddress_ntop(arg):
  '''
  3221225473  (network) -> '192.0.0.1'
  '''
  r = []
  for i in range(4):
    v = (arg >> (i * 8)) & 0xFF
    r.append('{0}'.format(v))

  r.reverse()
  return '.'.join(r)


def ipaddress_pton2(ip):
  return int(socket.inet_aton(ip).encode('hex'), 16)

def ipaddress_ntop2(arg):
  v = hex(arg)[2::]
  v = v.rstrip('L')
  return socket.inet_ntoa(v.decode('hex'))


def ipaddress_pton_unix(arg):
  '''
  inet_pton is only for unix
  '''
  return int(socket.inet_pton(socket.AF_INET,arg).encode('hex'),16)


class TestCase(unittest.TestCase):
  def test1(self):
    args = [u'192.168.0.1',  # 3232235521
            u'192.168.34.12',  # 3232244236
            ]

    for arg in args:
      # v = ipaddress.ip_address(arg)
      # print(int(v))
      # print(str(v))
      pass


    for arg in args:
      v1 = ipaddress_pton(arg)
      v2 = ipaddress_pton2(arg)
      self.assertEqual(v1,v2)

    for arg in args:
      v = ipaddress_pton(arg)
      r = ipaddress_ntop(v)
      self.assertEqual(arg, r)

    for arg in args:
      v = ipaddress_pton2(arg)
      r = ipaddress_ntop2(v)
      self.assertEqual(arg,r)



def entry():
  i = u'192.0.0.1'
  a = ipaddress.ip_address(i)

  print(int(a))
  print(str(a))

  v = 3221225473
  print socket.ntohl(v)


if __name__ == '__main__':
  #unittest.main()
  entry()
