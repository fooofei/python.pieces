# coding=utf-8

'''

    use itertools.tee to copy an generator
    适合多个 iterator 步差不大的, <10 的

    1 生成两个 generator 但是实例并没有增加
    2 两个 generator 持有同一份实例的引用 在一个 generator 中修改了一个实例 另一个 generator 也会受到修改影响
    3 官方警告使用 itertools.tee 分裂之后 母 generator 不再使用 https://docs.python.org/2/library/itertools.html
    4 官方建议 如果其中 1 个 iterator 走的太快 其他的 iterator 没走 使用 list() 比 tee() 更快
'''

import itertools
import sys
import unittest
import copy

count = 0


class Instance(object):
  def __init__(self, v):
    global count
    print ('instance init {}'.format(count))
    count += 1
    self._v = v

  @property
  def v(self):
    return self._v

  def __del__(self):
    print ('instance del')

  def __str__(self):
    return super(Instance, self).__str__()

  def __repr__(self):
    return '{}'.format(self.v)


class MyTestCase(unittest.TestCase):
  def test_fetch_iterator_value(self):
    a = [Instance(i) for i in range(10)]
    ai = iter(a)
    self.assertEqual(a, list(ai))
    self.assertEqual([], list(ai))

  def test_tee_iterator1(self):
    a = [Instance(i) for i in range(10)]

    ai = iter(a)

    ai1, ai2 = itertools.tee(ai)

    self.assertEqual(a, list(ai1))
    self.assertEqual([], list(ai))

  def test_tee_iterator2(self):
    a = [Instance(i) for i in range(10)]

    ai = iter(a)

    ai1, ai2 = itertools.tee(ai)

    self.assertEqual(a, list(ai1))
    self.assertEqual(a, list(ai2))

  def test_tee_iterator3(self):
    a = [Instance(i) for i in range(10)]

    ai = iter(a)

    ai1, ai2 = itertools.tee(ai)

    self.assertEqual(a, list(ai))

    self.assertEqual([], list(ai1))
    self.assertEqual([], list(ai2))

  def test_tee_iterator4(self):
    a = [Instance(i) for i in range(10)]
    ai = iter(a)
    ai1, ai2 = itertools.tee(ai)


    # this will effect a and list(ai2)
    for v in ai1:
      if v.v == 5:
        v._v = 55


    self.assertEqual(a, list(ai2))


if __name__ == '__main__':
  unittest.main()
