#coding=utf-8

'''
#define 	dl_restrict
#define 	RTLD_LAZY   0x1
#define 	RTLD_NOW   0x2
#define 	RTLD_LOCAL   0x4
#define 	RTLD_GLOBAL   0x8
#define 	RTLD_NOLOAD   0x10
#define 	RTLD_NODELETE   0x80
#define 	RTLD_NEXT   ((void *) -1)
#define 	RTLD_DEFAULT   ((void *) -2)


'''

import os
import sys
import ctypes


def entry():
    # if so has undefined symbol, this also can load success.
    # load 成功后，运行时当遇到未定义符号的函数会报错误 python: symbol lookup error: xxxx.so: undefined symbol: xxxx

    a = ctypes.CDLL('xxxxx.so',mode=1)

    # 这种 mode 直接报错
    # ctypes.CDLL('xxxx.so')
    # == ctypes.CDLL('xxxx.so',mode=2)


if __name__ == '__main__':
    entry()