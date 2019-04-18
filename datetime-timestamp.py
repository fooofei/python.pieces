#coding=utf-8

from datetime import datetime as DateTime
from timeit import default_timer as Time
from time import mktime
import unittest

def datetime2unix(dt):
    v = mktime(dt.timetuple())
    return int(v)

def datetime2unixmill(dt):
    v = mktime(dt.timetuple())
    return int(1000*v)


def unix2datetime(t):
    return DateTime.fromtimestamp(t)


class MyTest(unittest.TestCase):
    def test1(self):
        a = DateTime(year=2019, month=4, day=17)
        b = datetime2unixmill(a)
        self.assertEqual(b, 1555430400000)


if __name__ == '__main__':
    a = unix2datetime(1555430400)
    print(a)
