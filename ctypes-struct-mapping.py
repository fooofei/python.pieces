#coding=utf-8

'''
https://stackoverflow.com/questions/21483482/efficient-way-to-convert-string-to-ctypes-c-ubyte-array-in-python
'''

import os
import sys
import ctypes
import binascii

from ctypes import c_uint64
from ctypes import c_uint32
from ctypes import c_uint16
from ctypes import c_ubyte
from ctypes import c_uint8
from ctypes import c_long

class timespec(ctypes.Structure):
  _fields_=[('tv_sec', c_long), ('tv_nsec', c_long)]

class Flow(ctypes.Structure):
  _pack_ = 1
  _fields_=[
    ('v8',c_uint8),
    ('v16',c_uint16),
    ('v32',c_uint32),
    ('v64',c_uint64),
    ('v_ar', c_ubyte * 4),
    ('v_time', timespec),
  ]

  def __str__(self):
    v1 = '{} {} {} {}'.format(self.v8, self.v16, self.v32, self.v64)
    v2 ='[{}][{},{},{},{}]'.format(len(self.v_ar),self.v_ar[0], self.v_ar[1], self.v_ar[2], self.v_ar[3])
    v3 = '[{},{}]'.format(self.v_time.tv_sec, self.v_time.tv_nsec)
    return '{} {} {}'.format(v1,v2,v3)


def entry():

  a = Flow()
  a.v8=1
  a.v16=2
  a.v32=4
  a.v64=8
  a.v_ar[0]=11
  a.v_ar[1]=12
  a.v_ar[2]=13
  a.v_ar[3]=14
  a.v_time.tv_sec = 9
  a.v_time.tv_nsec = 10

  size = ctypes.sizeof(Flow)
  print(size)

  b = (binascii.hexlify(a))

  c = binascii.unhexlify(b)

  d = Flow.from_buffer_copy(c)

  e = ctypes.POINTER(Flow).from_buffer_copy(c)

  print(e[0])


if __name__ == '__main__':
    entry()