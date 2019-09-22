#coding=utf-8


import os
import sys

from ctypes import BigEndianStructure
from ctypes import LittleEndianStructure
from ctypes import Structure

from ctypes import c_uint8
from ctypes import c_uint16
from ctypes import c_uint32
from ctypes import sizeof
from ctypes import memmove
from ctypes import create_string_buffer
from ctypes import addressof
from ctypes import addressof
from ctypes import string_at
from ctypes import byref
from ctypes import cast
from ctypes import POINTER
from ctypes import pointer
from binascii import hexlify
from binascii import unhexlify


class BaseStructure(Structure):
    ''' 一个序列化和反序列化的范例  
        有了这个以后 再也不用 struct.pack struct.unpack 反人类的操作了 
    '''
    def pack(self):
        size = sizeof(self)
        buf = create_string_buffer(size)
        memmove(buf, addressof(self), size)
        return buf.raw

    def pack2(self):
        buf = string_at(byref(self), sizeof(self))
        return buf

    def pack3(self):
        return buffer(self)[::]

    @classmethod
    def unpack(cls, rawbytes):
        size = sizeof(cls)
        if (size != len(rawbytes)):
            raise ValueError("sizeof(self){} != len(bytes)".format(size, len(rawbytes)))
        return cls.from_buffer_copy(rawbytes)

    @classmethod
    def unpack2(cls, rawbytes):
        self=cls()
        cbuf = create_string_buffer(rawbytes)
        ins = cast(pointer(cbuf), POINTER(cls)).contents
        return ins



class BigEdnSt(BigEndianStructure):
    _pack_=1
    _fields_=[
        ('u8', c_uint8),
        ('u16', c_uint16),
        ('u32', c_uint32)
    ]

    def pack(self):
        return buffer(self)[::]

    @classmethod
    def unpack(cls, hexStream):
        a = unhexlify(hexStream)
        b = cls.from_buffer_copy(a)
        restBytes = a[sizeof(b)::]
        return b, hexlify(restBytes)

class LtlEdnSt(LittleEndianStructure):
    _pack_=1
    _fields_ = [
        ('u8', c_uint8),
        ('u16', c_uint16),
        ('u32', c_uint32)
    ]

    def pack(self):
        return buffer(self)[::]

    @classmethod
    def unpack(cls, hexStream):
        a = unhexlify(hexStream)
        b = cls.from_buffer_copy(a)
        restBytes = a[sizeof(b)::]
        return b, hexlify(restBytes)


def entry():
    be = BigEdnSt()
    be.u8 = 0x01
    be.u16 = 0x0203
    be.u32 = 0x04050607
    print('be = {}'.format(hexlify(be)))

    lt = LtlEdnSt()
    lt.u8 = 0x01
    lt.u16 = 0x0203
    lt.u32 = 0x04050607
    print('lt = {}'.format(hexlify(lt)))
    '''
    be = 01020304050607
    lt = 01030207060504
    '''


if __name__ == '__main__':
    entry()