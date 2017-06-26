#coding=utf-8

import os
import sys
import unittest
import types

class MyTestCase(unittest.TestCase):


    def test_1(self):
        l = [1, 2, 3, 4, 5]

        l2 = [v * v for v in l]

        self.assertIsInstance(l2, list)
        self.assertEqual(l2, [1, 4, 9, 16, 25])


    def test_2(self):
        l = [1, 2, 3, 4, 5]

        l2 = (v * v for v in l)

        self.assertIsInstance(l2, types.GeneratorType)

        self.assertEqual(list(l2),  [1, 4, 9, 16, 25])


if __name__ == '__main__':
    unittest.main()