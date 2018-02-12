#coding=utf-8

import subprocess
import unittest
import time

class Processes(object):
  '''
  不断的添加运行的命令， 通过 aging 老化执行结束的进程句柄
  不阻塞主线程
  '''

  def __init__(self):
    self._q=[]

  def push(self, *args, **kwargs):
    p = subprocess.Popen(*args, **kwargs)
    self._q.append(p)

  def aging(self):
    self._q[:] = [e for e in self._q if e.poll() is None]

  def __len__(self):
    return len(self._q)

  def wait(self):

    for e in self._q:
      while e.poll() is None:
        e.wait()


class TestCase(unittest.TestCase):

  def test_process(self):

    a = Processes()

    a.push(['sleep','1'])
    a.push(['sleep','4'])
    a.push(['sleep','1'])
    a.push(['sleep','1'])

    time.sleep(2)

    # Before aging, we got all
    self.assertEqual(4,len(a))
    a.aging()

    self.assertEqual(len(a), len(a._q))
    # After aging once, we got one left
    self.assertEqual(1,len(a))
    a.wait()

    # after all, we got 0
    a.aging()
    self.assertEqual(0, len(a))


if __name__ == '__main__':
    unittest.main()
