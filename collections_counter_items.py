#coding=utf-8

'''
the file shows how to count in python
Count 是 key 相同的累加求和
the old way and the use collections.Counter  way
'''

import os
import sys
from collections import Counter
from collections import defaultdict
import unittest

class MyTestCase(unittest.TestCase):

    def test_counter_1(self):
        a = ['a','a','b','b',
         'c','c','c']

        b = Counter(a)

        self.assertEqual(b.items(), [('a', 2), ('c', 3), ('b', 2)] )

    def test_counter_2(self):

        a = ['a', 'a', 'b', 'b',
         'c', 'c', 'c']

        b = Counter()

        for e in a :
            b.update({e:1})

        self.assertEqual(b.items(), [('a', 2), ('c', 3), ('b', 2)])


    def test_counter_3(self):
        b = Counter()

        b.update({'a': 4})
        b.update({'a': 7})
        b.update({'b': 2})
        b.update({'b': 2})
        b.update({'c': 1})
        b.update({'c': 0})

        self.assertEqual(b.items(), [('a', 11), ('c', 1), ('b', 4)])

    def test_counter_4(self):
        b = Counter()

        b.update(a = 4)
        b.update(a = 7)
        b.update(b = 2)
        b.update(b = 2)
        b.update(c = 1)
        b.update(c = 0)

        self.assertEqual(b.items(), [('a', 11), ('c', 1), ('b', 4)])

    def test_counter_error(self):
        ''' 请问 这可以说是 Counter() 的 bug 吗 '''
        b = Counter()
        b.update({'a': '4'})  # 首次使用时 b 为空 'a' 直接使用 dict 的构造方式(update())填充进去 值为 '4'
        b.update({'a': '7'})  # 取出 'a' 的值 '4' 在此基础上 + '7'， 为 '47'

        self.assertEqual(b.items(), [('a','47')]) # Python 3.6 is [('a','74')])

        with self.assertRaises(TypeError):
            b.update({'a':9})

        with self.assertRaises(TypeError):
            b.update({'b':'1'}) # b 不为空，使用dict 的 get(val,default=0) 的方式 + '1' ， 出现 0 + '1' 导致异常


    def test_counter_old_way(self):
        a = ['a', 'a', 'b', 'b',
             'c', 'c', 'c']

        b = {}

        for e in a:
            b.setdefault(e,0)
            b[e] += 1
        c = Counter(a)

        self.assertEqual(b.items(), c.items())


    def test_item_sum_count(self):
        import itertools
        a = ['a', 'a', 'b', 'b',
             'c', 'c', 'c']

        b = Counter(a)

        self.assertIsInstance(b.elements(), itertools.chain)

        with self.assertRaises(TypeError):
            len(b.elements())

        length = sum((1 for _ in b.elements()))

        length2 = sum(b.values())


        self.assertEqual(length, length2)
        self.assertEqual(length, len(a))



if __name__ == '__main__':
    unittest.main()