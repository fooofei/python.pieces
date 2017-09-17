# coding=utf-8
'''
the file shows how to assign a new list when pass to a function's param
'''
import os
import sys
import unittest
from copy import deepcopy

class MyTestCase(unittest.TestCase):

    def _not_change(self, l):
        l = sorted(l)


    def _change(self, l):
        l[::] = sorted(l)


    def test_not_change(self):
        l = ['b', 'a', 'c', 'f', 'e', 'd']
        l2 = deepcopy(l)
        self._not_change(l2)
        self.assertEqual(l2, l)


    def test_change(self):
        l = ['b', 'a', 'c', 'f', 'e', 'd']
        l2 = deepcopy(l)
        self._change(l2)
        self.assertEqual(l2, sorted(l))


if __name__ == '__main__':
    unittest.main()
