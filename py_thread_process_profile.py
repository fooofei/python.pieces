#coding=utf-8

'''
ref https://segmentfault.com/a/1190000007495352
    
1. much cpu --- use multi process, not others
2. much io --- use multi process, not others
3. much net --- use multi thread first

what is different :
1. pure python code and python+c is different, in python+c thread pool is usefull


'''

from __future__ import unicode_literals

import os
import requests
import time
from threading import Thread
from multiprocessing import Process


task_count = 10

def much_cpu(arg):
    c = 0
    x = 1
    y = 1
    while c < 100000 :
        c += 1
        x += x
        y += y


def much_io_write(arg):
    import random
    curpath = os.path.dirname(os.path.realpath(__file__))

    while 1:
        pw = os.path.join(curpath,'test_{}.txt'.format(random.randint(0,100)))
        if not os.path.exists(pw):
            break
    with open(pw,'w') as fw:
        for _ in range(5000000):
            fw.write('testwrite\n')


    return pw

def much_io_read(pw):
    c = None
    with open(pw, 'r') as fr:
        for l in fr:
            c = l
    os.remove(pw)

def _much_net():
    url = 'https://tieba.baidu.com/'
    try:
        response = requests.get(url)
        c = response.content
        return {'content':c}
    except Exception as er:
        return {'error':er}

def much_net(arg):
    for _ in range(0,3):
        _much_net()


class Profile(object):
    def __init__(self, a):
        self._a = a

    def execute(self, label, func, *args, **kwargs):
        times = []
        for _ in range(kwargs.pop('execute_count',3)):
            t = time.clock()
            func(*args,**kwargs)
            times.append(time.clock()-t)

        import sys
        print ('{} {} {}'.format(self._a, label, map(lambda e : '{:.3f}'.format(e),times)))
        sys.stdout.flush()



def profile_line():

    t = Profile(profile_line.__name__)
    f = lambda : [much_cpu(None) for _ in range(task_count)]
    t.execute('cpu',f)

    f = lambda : [much_io_read(much_io_write(None)) for _ in range(task_count)]
    t.execute('io', f)

    f = lambda : [much_net(None) for _ in range(task_count)]
    t.execute('net', f)



def _threading_thread_framework(target,args):
    ts = []
    for _ in range(task_count):
        th = Thread(target=target, args=args)
        ts.append(th)
        th.start()

    is_all_thread_exit = False
    while not is_all_thread_exit:
        is_all_thread_exit = True
        for th in ts:
            if th.is_alive():
                is_all_thread_exit = False

def much_io(arg):
    much_io_read(much_io_write(arg))

def profile_threading_thread():

    t = Profile(profile_threading_thread.__name__)

    #t.execute('cpu',_threading_thread_framework,target=much_cpu,args=(None,))

    # f = lambda a: much_io_read(much_io_write(None))
    t.execute('io',_threading_thread_framework,target=much_io,args=(None,))

    #t.execute('net',_threading_thread_framework,target=much_net,args=(None,))


def _multiprocessing_process_framework(target,args):
    ts = []
    for _ in range(task_count):
        th = Process(target=target, args=args)
        ts.append(th)
        th.start()

    is_all_thread_exit = False
    while not is_all_thread_exit:
        is_all_thread_exit = True
        for th in ts:
            if th.is_alive():
                is_all_thread_exit = False

def _process_io_func(arg):
    much_io_read(much_io_write(arg))

def profile_multiprocessing_process():
    t = Profile(profile_multiprocessing_process.__name__)

    t.execute('cpu',_multiprocessing_process_framework, target=much_cpu, args=(None,))

    t.execute('io',_multiprocessing_process_framework, target=_process_io_func, args=(None,))

    t.execute('net',_multiprocessing_process_framework, target=much_net, args=(None,))


def _futures_threadpool_framework(target,args):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=task_count) as pool:
        r = pool.map(target,args)
        pool.shutdown(wait=True)
        return list(r)


def profile_futures_threadpool():
    t = Profile(profile_futures_threadpool.__name__)

    t.execute('cpu',_futures_threadpool_framework, target=much_cpu,args=range(task_count))

    f = lambda a: much_io_read(much_io_write(a))
    t.execute('io',_futures_threadpool_framework, target=f,args=range(task_count))

    t.execute('net',_futures_threadpool_framework, target=much_net,args=range(task_count))


def entry():

    profile_line()
    print ('')
    profile_threading_thread()
    print ('')
    profile_multiprocessing_process()
    print ('')
    profile_futures_threadpool()
    print ('')
    profile_python_c_line()
    print ('')
    profile_python_c_threadpool()

def _get_obj():
    from libexportqex import QexScanner
    scan = QexScanner(qex_save_dir=r'')
    scan.set_config_use_local_qvm()
    return scan

def _get_data():
    import io_in_out
    p=r'samples'
    return io_in_out.io_iter_files_from_arg([p])

def _thread_func(obj,data):
    obj.scan_path_w(data)

def map_stub(f,d):
    for e in d:
        f(data=e)

def profile_python_c_line():
    from functools import partial
    f = partial(_thread_func,obj=_get_obj())
    t = Profile(profile_python_c_line.__name__)
    t.execute('io',map_stub,f,_get_data(),execute_count=1)

def profile_python_c_threadpool():
    import io_in_out

    t = Profile(profile_python_c_threadpool.__name__)
    t.execute('io',io_in_out.io_thread_map_one_ins,
              execute_count=1,
              thread_data=_get_data(),
              ins_generator_func=_get_obj,
              thread_func=_thread_func,
              max_workers=task_count)


if __name__ == '__main__':
    entry()


'''
profile_line cpu [u'40.586', u'40.518', u'40.489']
profile_line io [u'33.595', u'33.665', u'34.732']
profile_line net [u'10.420', u'10.286', u'9.987']

profile_threading_thread cpu [u'46.130', u'42.408', u'42.596']
profile_threading_thread io [u'204.598', u'200.775', u'201.306']
profile_threading_thread net [u'1.159', u'1.161', u'1.174']

profile_multiprocessing_process cpu [u'11.869', u'12.523', u'11.826']
profile_multiprocessing_process io [u'10.708', u'10.632', u'10.578']
profile_multiprocessing_process net [u'1.601', u'1.666', u'1.576']

profile_futures_threadpool cpu [u'42.381', u'42.600', u'42.425']
profile_futures_threadpool io [u'185.027', u'181.874', u'181.583']
profile_futures_threadpool net [u'1.328', u'1.564', u'1.406']

profile_python_c_line io [u'6.413']

profile_python_c_threadpool io [u'1.962']
'''