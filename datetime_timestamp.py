# coding=utf-8

from datetime import datetime
from timeit import default_timer as time
from time import mktime
import unittest
from calendar import nextmonth
from calendar import prevmonth
from calendar import monthlen
from datetime import timedelta


def datetime2unix(dt):
    v = mktime(dt.timetuple())
    return int(v)


def datetime2unixmill(dt):
    return 1000 * datetime2unix(dt)


def unix2datetime(t):
    return datetime.fromtimestamp(t)


def monthdelta(date: datetime, delta: int) -> datetime:
    '''
    same with timedelta, but add or sub with months
    :param date:
    :param delta:
    :return:
    '''
    new_year, new_month = date.year, date.month
    func_offmonth = prevmonth if delta < 0 else nextmonth
    for _ in range(0, abs(delta)):
        new_year, new_month = func_offmonth(new_year, new_month)
    new_day = min(date.day, monthlen(new_year, new_month))
    return date.replace(day=new_day, month=new_month, year=new_year)


def from_mysql_todays(days):
    '''
    :param days: int
    :return: datetime
    '''
    return datetime.fromordinal(days - 365)


def from_str(dt_str):
    '''
    a = datetime.now()
    b = from_str(str(a.isoformat()))
    :param dt_str:
    :return:
    '''
    dt, _, us = dt_str.partition(".")
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us = int(us.rstrip("Z"), 10)
    return dt + timedelta(microseconds=us)


class MyTest(unittest.TestCase):
    def test1(self):
        a = datetime(year=2019, month=4, day=17)
        b = datetime2unixmill(a)
        self.assertEqual(b, 1555430400000)

    def test2(self):
        a = datetime(year=2019, month=1, day=31)
        b = monthdelta(a, 1)
        self.assertEqual(b, datetime(year=2019, month=2, day=28))

    def test_mysql_todays(self):
        a = 737928
        b = from_mysql_todays(a)
        self.assertEqual(b, datetime(year=2020, month=5, day=18))


if __name__ == '__main__':
    a = unix2datetime(1555430400)
    print(a)
