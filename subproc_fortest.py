#coding=utf-8
'''
此文件用来给 subprocess_idioms.py 做辅助测试文件
'''

import sys
import time

def entry():
    count =0

    while True:
        sys.stdout.write('stdout from subproc count={c}\n'.format(c=count))
        sys.stdout.flush()
        count +=1
        if count >2:
            # exit process
            break
        time.sleep(2)


if __name__ == '__main__':
    entry()
