# coding=utf-8

from sched import scheduler
from threading import Event
from time import time
import signal

g_exit_event = Event()

def sleep(t):
    g_exit_event.wait(timeout=t)


def shutdown(_signo, _stack_frame):
    g_exit_event.set()


def sched_func(s, arg):
    print("{} enter sched func arg={}".format(time(), arg))
    sleep(3)
    print("{} leave sched func".format(time()))


def main():
    # 这个不好用 不推荐使用
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    s = scheduler(delayfunc=sleep)
    s.enter(3, 0, sched_func, (s, 3,))
    s.enter(2, 0, sched_func, (s, 2,))
    print("enter run")
    s.run(blocking=True) # run return 之后，队列中的事件就不执行了
    print("leave run")

    #

    print("wait on exit event")
    g_exit_event.wait()

if __name__ == '__main__':
    main()