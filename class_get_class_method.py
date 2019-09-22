# coding=utf-8

import os
import sys
import unittest


def get_class_methods(klass):
    '''
    :param klass:
    :return: list / all callable methods by user defined
    '''
    ret = dir(klass)
    if hasattr(klass, '__bases__'):
        for base in klass.__bases__:
            ret.extend(get_class_methods(base))

    ret = filter(lambda m: not m.startswith('_'), ret)
    o = klass()
    return filter(lambda v: callable(getattr(o, v)), ret)


class Test(object):
    def __init__(self):
        print('test_init')

    def foo1(self):
        print('test_foo1')

    def foo2(self):
        print('test_foo2')


class MyTestCase(unittest.TestCase):
    def test1(self):
        method_names = get_class_methods(Test)
        method_names = list(method_names)
        self.assertEqual(len(method_names),2)
        self.assertEqual(method_names,["foo1", "foo2"])

if __name__ == '__main__':
    unittest.main()