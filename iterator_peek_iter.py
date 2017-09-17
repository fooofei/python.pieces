# coding=utf-8

import unittest


def peek_iter(iter_ins):
  '''
  iter_ins.next() 会把值取出来，该函数取值后，再拼装回去，做到窥探的目的
  :param iter_ins:  iterable, such as iter([1,2,3])
  :return:
  '''
  import itertools
  r = iter_ins.next()
  iter_ins = itertools.chain([r], iter_ins)
  return iter_ins, r


class MyTestCase(unittest.TestCase):
  def test1(self):
    a = [1, 2, 3]
    ai = iter(a)

    ai, value = peek_iter(ai)
    self.assertEqual(value,a[0])

    ai,value = peek_iter(ai)
    self.assertEqual(value,a[0])


if __name__ == '__main__':
  unittest.main()
