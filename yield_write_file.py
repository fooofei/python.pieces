#coding=utf-8

import os
import sys


def yield_write_file():
    ''' limit Cannot return value '''
    curpath = os.path.dirname(os.path.realpath(__file__))
    p = os.path.join(curpath,'1')
    with open(p, 'wb') as fw:
        while True:
            c = yield
            if c is None:
                break
            fw.write(c)



    with open(p,'rb') as fr:
        print('your write is :{}'.format(fr.read()))

    os.remove(p)

def entry():

    f = yield_write_file()
    f.next()
    f.send('nihao\n')
    f.send('wobuhao')
    try: f.send(None)
    except StopIteration: pass


if __name__ == '__main__':
    entry()