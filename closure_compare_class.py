#coding=utf-8

'''
See A class with one member, one method

is can equivalent with a closure.

'''

import unittest

class MyObject(object):
    def __init__(self):
        self._value = 1

    def increment(self):
        self._value += 1
        return self._value


def closure_increment():

    def _inner():
        _value[0] += 1
        return _value[0]

    _value=[1]
    return _inner  # Cannot be _inner()




class MyTestCase(unittest.TestCase):

    def test_equal(self):

        obj = MyObject()
        v1 = []
        for _ in range(10):
            v1.append(obj.increment())


        closure = closure_increment()
        v2 = []
        for _ in range(10):
            v2.append(closure())

        self.assertEqual(v1, v2)



if __name__ == '__main__':
    unittest.main()
