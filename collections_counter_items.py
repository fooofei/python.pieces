#coding=utf-8

'''

    Python 中计数的方式
    
    如果不使用 collections.Counter 的话，会是这么用 counter_list_old_way()

'''

import os
import sys
from collections import Counter
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
        b = Counter()
        b.update({'a': '4'})  # 首次使用时 b 为空 'a' 直接使用 dict 的构造方式(update())填充进去 值为 '4'
        b.update({'a': '7'})  # 取出 'a' 的值 '4' 在此基础上 + '7'， 为 '47'

        self.assertEqual(b.items(), [('a','47')])

        with self.assertRaises(TypeError):
            b.update({'a':9})

        with self.assertRaises(TypeError):
            b.update({'b':'1'}) # b 不为空，使用dict 的 get(val,default=0) 的方式 + '1' ， 出现 0 + '1' 导致异常


    def test_counter_old_way(self):
        a = ['a', 'a', 'b', 'b',
             'c', 'c', 'c']

        b = {}

        for e in a:
            if not e in b:
                b[e] = 1
            else:
                b[e] += 1


        c = Counter(a)

        self.assertEqual(b.items(), c.items())

        self.assertEqual(b.items(), [('a',2),('b',2),('c',3)])




def sum_all_item_count():
    from collections import Counter
    a = ['a', 'a', 'b', 'b',
         'c', 'c', 'c']

    b = Counter(a)

    # b.elements() is itertools.chain object
    '''
    itertools.chain(*iterables)
    # 把元素再拆分的意思
    def chain(*iterables):
        # chain('ABC', 'DEF') --> A B C D E F
        for it in iterables:
            for element in it:
                yield element
    '''

    print (sum(1 for _ in b.elements()))


def entry():
    counter_list()
    counter_list2()
    counter_update_items()
    counter_update_items2()
    counter_list_old_way()
    sum_all_item_count()

if __name__ == '__main__':
    unittest.main()