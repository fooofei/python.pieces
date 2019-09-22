# coding=utf-8

'''
the file shows an error use, cause an infinite loop
'''

import os
import sys
import types
import unittest
import itertools

from collections import Iterable as IterableType


class MyClass_null(object):
    def __init__(self):
        self._v = {'a': 1,
                   'b': 2}


class MyClass_getitem(object):
    def __init__(self):
        self._v = {'a': 1,
                   'b': 2}

    def __getitem__(self, item):
        # print ('call MyClass2:__getitem__({})'.format(item))
        return self._v.get(item, None)


class MyClass_getitem_fix(object):
    def __init__(self):
        self._v = {'a': 1,
                   'b': 2}

    def __getitem__(self, item):
        if not self._v.has_key(item):
            raise IndexError('')
        return self._v.get(item)


def is_iterable_by_collections(obj):
    return isinstance(obj, IterableType)


def is_iterable_by_iter(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


class MyTestCase(unittest.TestCase):
    def test_iterable(self):
        o_null = MyClass_null()
        o_getitem = MyClass_getitem()

        self.assertTrue(not is_iterable_by_collections(o_null))
        self.assertTrue(not is_iterable_by_collections(o_getitem))

        self.assertTrue(not is_iterable_by_iter(o_null))
        self.assertTrue(is_iterable_by_iter(o_getitem))

    def test(self):
        o_null = MyClass_null()
        o_getitem = MyClass_getitem()

        with self.assertRaises(TypeError):
            for i in o_null:
                pass

        for i, c in zip(range(1000), o_getitem):
            pass

        self.assertEqual(i, 999)

    def test_instance_method(self):
        a = dir(MyClass_getitem())
        b = dir(MyClass_null())

        a = set(a)
        b = set(b)

        self.assertEqual(a - b, set(['__getitem__']))

    def test_fix(self):

        o_fix = MyClass_getitem_fix()

        '1' in o_fix


if __name__ == '__main__':
    unittest.main()
