#coding=utf-8

'''


'''

import os
import sys
import binascii
import socket


def entry():
    addr = ('127.0.0.1', 44444)
    cfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cfd.connect(addr)

    r = cfd.send('hello')

    print('send to {} ret={}'.format(addr, r))

if __name__ == '__main__':
    entry()
