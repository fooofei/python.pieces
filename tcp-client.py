#coding=utf-8

'''


'''

import os
import sys
import binascii
import socket
import time

def entry():
    addr = ('127.0.0.1', 44444)
    cfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cfd.connect(addr)

    try:
        while True:
            r = cfd.send('hello')
            print('send to {} ret={}'.format(addr, r))
            time.sleep(1)
    except socket.error as er:
        print('er={0} errno={1}'.format(er, socket.errno))
        if (er.errno == socket.errno.EPIPE):
            print('errno=EPIPE server is not connected')


if __name__ == '__main__':
    entry()
