# coding=utf-8


import os
import sys
import unittest
import itertools
import io

def error1():
    '''
        for _ in xrange(size):
    OverflowError: Python int too large to convert to C long
    '''
    curpath = os.path.relpath(__file__)
    curpath = os.path.dirname(curpath)
    fn = os.path.join(curpath,'__temp.txt')
    if os.path.exists(fn):
        os.remove(fn)

    size = 0xFFFFFFFF
    size = long(size)
    print('[+] the size is {s}'.format(s=size))
    with open(fn,'wb') as fw:
        for _ in xrange(size):
            fw.write('1')


def test_write_4gb_file():
    '''
    Difference in open() with io.open() ?
    they are same
    '''

    curpath = os.path.relpath(__file__)
    curpath = os.path.dirname(curpath)
    fn = os.path.join(curpath,'__temp.txt')
    if os.path.exists(fn):
        os.remove(fn)

    nrange = long(0x80000)
    count = 0x2000
    size = nrange*count
    print('[+] the size is {s}'.format(s=size))
    isize = long(0)
    with open(fn,'wb') as fw:
        for _ in itertools.count(start=0, step=1):
            fw.write('1'*count)
            isize += count
            if isize>= size:
                break



if __name__ == '__main__':
    test_write_4gb_file()
