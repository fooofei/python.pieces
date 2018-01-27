#coding=utf-8

'''
 the file shows ipaddress convert

 ipaddress is a Python 3.3+ package

'''

import os
import sys
import ipaddress
import unittest


def ipaddress_ptoh(arg):
  '''
  '192.0.0.1' -> 3221225473  (host)
  '''
  pvs = arg.split('.')
  r=0
  for pv in pvs:
    r = (r<<8) + int(pv,10)

  return r

def ipaddress_htop(arg):
  '''
  3221225473  (host) -> '192.0.0.1'
  '''
  r = []
  for i in range(4):
    v = (arg>>(i*8))&0xFF
    r.append('{0}'.format(v))

  r.reverse()
  return '.'.join(r)


class TestCase(unittest.TestCase):
  def test1(self):
    args=[u'192.168.0.1', # 3232235521
        u'192.168.34.12', #3232244236
          ]

    for arg in args:
      #v = ipaddress.ip_address(arg)
      #print(int(v))
      #print(str(v))
      pass

    for arg in args:
      v = ipaddress_ptoh(arg)
      v2 = ipaddress_htop(v)
      self.assertEqual(arg,v2)

def entry():
  i = u'192.0.0.1'
  a = ipaddress.ip_address(i)

  print(int(a))
  print(str(a))

if __name__ == '__main__':
    unittest.main()
