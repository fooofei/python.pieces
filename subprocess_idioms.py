# coding=utf-8

'''

1 use subprocess.communicate() to send/get data/stdout from subprocess

2 subprocess.Popen, shell 参数:
            shell = False (default) , 执行参数应该是 list, 封装为 [<待执行二进制>, <arg0>,<arg1>,...]
                    更加 Pythonic 的使用方式，对执行参数更好控制
            shell = True, 执行参数可以是 str, 可以传递 '{} {} {}'.format(<待执行二进制>, <arg0>,<arg1>)
                把整个字符串直接在 shell 执行，容易被利用

    一个未解决的疑问
        subprocess.Popen will error on posix call curl
      subprocess.Popen(['curl',
                  '-F"file=@{0}"'.format(path_zip),
                   '-F"md5={0}"'.format(md5),
                   '-F"module=xxx"',
                   'http://xxx/update/up.php'], stdout=subprocess.PIPE)

      or
      subprocess.Popen(['curl',
                  '--form','"file=@{0}"'.format(path_zip),
                   '--form','"md5={0}"'.format(md5),
                   '--form','"module=xxx"',
                   'http://xxx/update/up.php'
                   ], stdout=subprocess.PIPE)

      all fail, error message is curl: (26) failed creating formpost data
      so we must use
      out = subprocess.Popen(
      'curl --form "file=@{0}" --form "md5={1}" --form "module=xxx" http://xxx/update/up.php'.format(path_zip,md5),
      shell=True, stdout=subprocess.PIPE).communicate()[0]

3 执行参数中 escape 相关: pipes.quote()

4
  show subprocess's stdout/stderr realtime
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  proc.stdout.readline() 有行的时候 会不阻塞 一行行读取，没值的时候就阻塞
  proc.stdout.readlines() 直接阻塞
  看看这个库 https://github.com/pexpect/pexpect/blob/master/pexpect/run.py
  学习这个 https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python/

  for line in iter(p.stdout.readline, b''):
            sys.stdout.write(line)

  这样也是阻塞，要配合 thread+queue 才行

5 运行的时候发现的，如果对此脚本使用 CTRL+C ，那么这个脚本的 subprocess 也会收到 CTRL+C
  然后结束子进程结束

'''

import subprocess
import unittest
import time
import timeit
import os
import threading
import sys

try:
    import Queue as mQueue
except ImportError:
    import queue as mQueue  # python 3.x

curpath = os.path.realpath(__file__)
curpath = os.path.dirname(curpath)


def popen_isalive(p):
    ''' 进程是否还在存活
    '''
    return p.poll() is None


def popen_list_aging(plist):
    '''已经死掉的进程从 list 中移除，即老化
    '''
    plist[:] = [e for e in plist if popen_isalive(e)]


def popen_list_waitall(plist):
    ''' 等待所有进程结束
    '''
    for e in plist:
        while e.poll() is None:
            e.wait()


def popen_timeout_wait(popen_ins, timeout):
    '''
    :param popen_ins: the return value of subprocess.Popen()
    :param timeout:
    :return: True for finish in time, False for run out time.
    '''

    start = timeit.default_timer()

    while popen_ins.poll() is None:  # is alive
        time.sleep(0.5)
        now = timeit.default_timer()
        # now = datetime.datetime.now()
        # if(now-start).seconds > timeout:
        if (now - start) > timeout:
            return False
    return True


def popen_kill(popen_ins):
    ''' kill process created by subprocess.Popen()
    :param popen_ins:
    :return:  None
    '''
    if popen_ins.poll() is None:
        # print('kill proc {}'.format(popen_ins.pid))
        # popen_ins.terminate()
        popen_ins.kill()

    while popen_ins.poll() is None:
        # print('fail kill, trying') # will be many times
        # if too fast, will be error OSError: [Errno 3] No such process
        os.kill(popen_ins.pid, 9)
        time.sleep(3)



def popen_queue_get_nowait(pq):
    ''' 非阻塞 从 Popen 绑定的队列取 output
   :param pq: 与 Popen 绑定的 Queue
   :return:
   '''
    out = []
    try:
        while True:
            line = pq.get_nowait()
            out.append(line)

    except mQueue.Empty:
        pass
    return out


def _popen_bind_realtime_stdout_thread_func(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def popen_bind_realtime_stdout(popen_ins):
    ''' 非阻塞 实时显示子进程的 stdout
    MUST use Popen(stdout=PIPE)
    '''
    q = mQueue.Queue()
    t = threading.Thread(target=_popen_bind_realtime_stdout_thread_func, args=(popen_ins.stdout, q))
    t.daemon = True
    t.start()
    return q

def test_popen_timeout(*args, **kwargs):
    '''
    when wrap subprocess.Popen() as this,
    the Popen() param will not have auto complete
    '''
    timeout = kwargs.pop('timeout', None)
    p_ins = subprocess.Popen(*args, **kwargs)

    if timeout is not None:
        if not popen_timeout_wait(p_ins, timeout):
            # timeout
            popen_kill(p_ins)
    return p_ins


def test_amr2avi():
    '''amr 批量转换为 avi
    此函数可以学习
    '''
    pathf = r''
    runexe = r''
    for e in os.listdir(pathf):
        if e.endswith('.amr'):
            cmd = '{0} {1}'.format(runexe, os.path.join(pathf, e))
            # no wait
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
            p.communicate(input='\n')  # 这里需要向子进程中填入 \n 来继续运行，是因为子程序是这样写的


def test_get_popen_args():
    ''' only Python3, not for Python2 '''
    args = ['ls', '.']
    p = subprocess.Popen(args)
    print('the args is {}'.format(p.args))  # Python3


def test_check_output(*args, **kwargs):
    ''' such as run _exec_check_output(['svn', 'up'],stderr=subprocess.STDOUT) '''
    v = subprocess.check_output(*args, **kwargs)
    v = v.rstrip()
    v = v.decode('utf-8')
    return v


class TestCase(unittest.TestCase):

    def test_process_age(self):
        process_list = []

        for c in [['sleep', '1'], ['sleep', '4'], ['sleep', '1'], ['sleep', '1']]:
            process_list.append(subprocess.Popen(c))

        time.sleep(2)

        # Before aging, we got all
        self.assertEqual(4, len(process_list))
        popen_list_aging(process_list)

        # After aging once, we got one left
        self.assertEqual(1, len(process_list))
        popen_list_waitall(process_list)

        # after all, we got 0
        popen_list_aging(process_list)
        self.assertEqual(0, len(process_list))

    def test_realtime_stdout(self):
        '''
        An output:
        [+] exec python D:\source\GitHub\py_pieces\subproc_fortest.py pid=14884
        [+] test_realtime_stdout is checking, we not blocked count=1
        [+] we get out put from python D:\source\GitHub\py_pieces\subproc_fortest.py
        ->stdout from subproc count=0
        [+] test_realtime_stdout is checking, we not blocked count=2
        [+] test_realtime_stdout is checking, we not blocked count=3
        [+] we get out put from python D:\source\GitHub\py_pieces\subproc_fortest.py
        ->stdout from subproc count=1
        [+] test_realtime_stdout is checking, we not blocked count=4
        [+] test_realtime_stdout is checking, we not blocked count=5
        [!] subproc pid=14884 arg=python D:\source\GitHub\py_pieces\subproc_fortest.py is dead, we exit

        :return:
        '''
        cmd = ['python',os.path.join(curpath,'subproc_fortest.py')]

        p = subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE,bufsize=1,
                             close_fds='posix' in sys.builtin_module_names)
        # if `stdout=subprocess.STDOUT, stderr=subprocess.STDOUT`
        #   will error IOError: [Errno 9] Bad file descriptor

        # bufsize default is 0, it work
        # bufsize is 1, it work
        # bufsize is -1, use systemdefault, it work

        print('[+] exec {c} pid={p}'.format(c=subprocess.list2cmdline(cmd),p=p.pid))
        pq = popen_bind_realtime_stdout(p)

        count =0

        while True:

            out = popen_queue_get_nowait(pq)

            if not popen_isalive(p):
                print('[!] subproc pid={p} arg={a} is dead, we exit'
                    .format(p=p.pid,a=subprocess.list2cmdline(cmd)))
                break

            if out:
                print('[+] we get out put from {c}'.format(c=subprocess.list2cmdline(cmd)))
                out = map(str,out)
                out = map(lambda e:'->'+e,out)
                sys.stdout.write(''.join(out))

            count +=1
            sys.stdout.write('[+] test_realtime_stdout is checking, we not blocked count={c}\n'.format(c=count))
            sys.stdout.flush()

            time.sleep(1)


if __name__ == '__main__':
    unittest.main()
