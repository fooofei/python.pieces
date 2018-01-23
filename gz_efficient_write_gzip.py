#coding=utf-8

'''
the file shows a more efficient way to write a gzip file

recommended use io.BufferedWriter

'''

import os
import sys

curpath = os.path.dirname(os.path.realpath(__file__))

def write_file_with_clock(f_stream):
    import time

    t = time.clock()
    for i in range(0, 1000000):
        f_stream.write(b'hello %d\n' % i)
    return time.clock()-t


def write_gzip_raw():
    import gzip

    pw = os.path.join(curpath,'test.gz')
    if os.path.exists(pw):
        os.remove(pw)

    with gzip.open(pw,'wb',compresslevel=1) as fw:
        r = write_file_with_clock(fw)

    return (write_gzip_raw.__name__,
                                os.path.getsize(pw),
                                r)

def write_gzip_with_io_bufferwriter():
    import gzip
    import io

    pw = os.path.join(curpath, 'test2.gz')
    if os.path.exists(pw):
        os.remove(pw)

    with gzip.open(pw, 'wb', compresslevel=1) as fw:
        with io.BufferedWriter(fw) as f:
            r = write_file_with_clock(f)

    return (write_gzip_with_io_bufferwriter.__name__,
                                os.path.getsize(pw),
                                r)


def test():
    r = write_gzip_raw()
    print ('method:{} >size:{} >time:{}'.format(*r))
    r = write_gzip_with_io_bufferwriter()
    print ('method:{} >size:{} >time:{}'.format(*r))

def entry():
    i = 0
    while i<4:
        test()
        i+= 1

if __name__ == '__main__':
    entry()

'''
 profile
 
 system info 
    cpu : i5
    memory: 20GB
    
  Python 2.7.12
        method:write_gzip_raw >size:2436049 >time:3.51380212559
        method:write_gzip_with_io_bufferwriter >size:2436050 >time:1.23108032783
        method:write_gzip_raw >size:2436049 >time:3.56025661338
        method:write_gzip_with_io_bufferwriter >size:2436050 >time:1.23028590782
        method:write_gzip_raw >size:2436049 >time:3.58649075464
        method:write_gzip_with_io_bufferwriter >size:2436050 >time:1.22703927328
        method:write_gzip_raw >size:2436049 >time:3.58563379451
        method:write_gzip_with_io_bufferwriter >size:2436050 >time:1.22965441286
        
 
  Python 3.6.0
        method:write_gzip_raw >size:2436049 >time:2.8157314404948304
        method:write_gzip_with_io_bufferwriter >size:2436050 >time:0.6853657378869391
        method:write_gzip_raw >size:2436049 >time:2.8610015144332994
        method:write_gzip_with_io_bufferwriter >size:2436050 >time:0.6860437370389594
        method:write_gzip_raw >size:2436049 >time:2.8739492456377462
        method:write_gzip_with_io_bufferwriter >size:2436050 >time:0.6817669543085003
        method:write_gzip_raw >size:2436049 >time:2.8587924046134745
        method:write_gzip_with_io_bufferwriter >size:2436050 >time:0.6853724729778534
 
'''