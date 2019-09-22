#coding=utf-8

'''

计秒应该使用 timeit.default_time()
timeit.default_timer() is a cross platform use

'''


import timeit
import time

def test_time():
  delay=3
  t1 = timeit.default_timer()
  time.sleep(delay)
  t2 = timeit.default_timer()

  t3 = t2-t1
  print('time delta = {}'.format(t3))


if __name__ == '__main__':
    test_time()