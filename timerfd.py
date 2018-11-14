#coding=utf-8

__all__ = [
	"TFD_CLOEXEC",
	"TFD_NONBLOCK",

	"TIMER_ABSTIME",

	"CLOCK_REALTIME",
	"CLOCK_MONOTONIC",

	"timespec",
	"itimerspec",

	"timerfd",
]


from ctypes import Structure
from ctypes import c_long
from ctypes import CDLL
from ctypes.util import find_library as c_find_library
from ctypes import get_errno
from os import strerror
from ctypes import pointer

TFD_CLOEXEC         = 0o02000000
TFD_NONBLOCK        = 0o00004000

TIMER_ABSTIME   = 0x00000001

CLOCK_REALTIME  = 0
CLOCK_MONOTONIC = 1


libc = CDLL(c_find_library("c"), use_errno=True)


def errcheck(result, func, argu):
    if result <0:
        errno = get_errno()
        raise OSError(errno, strerror(errno))
    return result

class timespec(Structure):
    _fields_ = [
        ('tv_sec', c_long),
        ('tv_nsec', c_long),
    ]
    def _str(self):
        s = 'tv_sec={0}'.format(self.tv_sec)
        ns = 'tv_nsec={0}'.format(self.tv_nsec)
        return '{0} {1}'.format(s, ns)
    def __str__(self):
        return self._str()
    def __repr__(self):
        return 'timerfd.timespec({0})'.format(self._str())

class itimerspec(Structure):
    _fields_=[
        ('it_interval', timespec),
        ('it_value', timespec),
    ]

    def _str(self):
        v1 = 'it_interval={0}'.format(self.it_interval)
        v2 = 'it_value={0}'.format(self.it_value)
        return '{0} {1}'.format(v1, v2)

    def __str__(self):
        return self._str()
    def __repr__(self):
        return 'timerfd.itimerspec({0})'.format(self._str())


class timerfd(object):
    def __init__(self):
        self._fileno = -1

    @property
    def fileno(self):
        return self._fileno

    def create(self, clock_id, flags):
        self.close()
        self._fileno = libc.timerfd_create(clock_id, flags)
        if self.fileno <0:
            errno = get_errno()
            raise OSError(errno, strerror(errno))

    def settime(self, flags, fstval, interval):
        n = itimerspec()
        n.it_value.tv_sec = fstval[0]
        n.it_value.tv_nsec = fstval[1]
        n.it_interval.tv_sec = interval[0]
        n.it_interval.tv_nsec = interval[1]
        o = itimerspec()

        rc = libc.timerfd_settime(self.fileno,flags,pointer(n),pointer(o))
        if rc !=0 :
            errno = get_errno()
            raise OSError(errno, strerror(errno))

    def gettime(self):
        cur = itimerspec()
        rc = libc.timerfd_gettime(self.fileno, pointer(cur))
        if rc !=0 :
            errno = get_errno()
            raise OSError(errno, strerror(errno))
        return ((cur.it_value.tv_sec,cur.it_value.tv_nsec),
                (cur.it_interval.tv_sec, cur.it_interval.tv_nsec))

    def close(self):
        if self.fileno >0:
            libc.close(self.fileno)
            self._fileno=-1


    def __del__(self):
        self.close()



def log(start, s):
    import time
    t = time.time()-start
    t = int(t)
    print('{} s {}'.format(t, s))

def example():
    from time import sleep
    from select import epoll
    from select import EPOLLIN
    from random import randint
    import time
    from os import read as fd_read
    sched = timerfd()
    sched.create(CLOCK_MONOTONIC, TFD_NONBLOCK | TFD_CLOEXEC)
    sched.settime(0, (3,0), (3,0))
    poll = epoll()
    poll.register(sched.fileno, EPOLLIN)
    start= time.time()
    while True:
        log(start, 'into poll')
        evs = poll.poll(-1,10)
        log(start, 'over poll')
        for fileno, ev in evs:
            assert fileno == sched.fileno
            if ev & EPOLLIN:
                r = fd_read(fileno,16)
                log(start, 'read {} from {}'.format(r, fileno))
                wk = randint(0,3)
                log(start, 'goto work {}'.format(wk))
                sleep(wk)
                log(start, 'work done')
            print('---------------------------------------------')




if __name__ == '__main__':
    example()
