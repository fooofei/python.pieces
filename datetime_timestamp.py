# coding=utf-8

from datetime import datetime
from timeit import default_timer as time
from time import mktime
import unittest
from calendar import _prevmonth as prevmonth
from calendar import _monthlen as monthlen
from datetime import timedelta
from calendar import _nextmonth as nextmonth
from iso8601 import parse_date as parse_iso8601
from rfc3339 import format as format_rfc3389
from rfc3339 import format_millisecond as format_rfc3389_mill
from rfc3339 import format_microsecond as format_rfc3389_micro


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


def parse_gmt(date_str):
    '''
    parse datetime like "2021-01-07T08:53:22.022GMT" to datetime.datetime(2021, 1, 7, 8, 53, 22, 22000)
    :param date_str:
    :return:
    '''
    date_str = date_str.rstrip("GMT")
    return parse_iso8601(date_str)


def close_at(a, b):
    '''
    时间是否接近
    a b are all datetime
    :param a:
    :param b:
    :return:
    '''
    a = a.replace(tzinfo=None)
    b = b.replace(tzinfo=None)
    c = b - a
    return abs(int(c.total_seconds())) < 15


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

    def test_ios8601(self):
        src1 = datetime.now().astimezone()
        a = src1.isoformat()  # 2021-01-10T21:27:54.287055+08:00
        dst1 = parse_iso8601(a)
        self.assertEqual(src1, dst1)

    def test_rfc3339(self):
        src1 = datetime.now().astimezone()
        a = format_rfc3389(src1)  # 2021-01-10T21:28:24+08:00
        dst1 = parse_iso8601(a)
        # 等于去掉毫秒
        src1 = src1.replace(microsecond=0)
        self.assertEqual(src1, dst1)

    def test_rfc3339_2(self):
        src1 = datetime.now().astimezone()
        a = format_rfc3389_micro(src1)  # 2021-01-10T21:28:38.490201+08:00
        dst1 = parse_iso8601(a)
        self.assertEqual(src1, dst1)

    def test_parse_gmt(self):
        a = "2021-01-07T08:53:22.022GMT"
        a1 = "2021-01-07 08:53:22.022000+00:00"
        b = parse_gmt(a)
        b1 = parse_iso8601(a1)
        self.assertEqual(b, b1)


if __name__ == '__main__':
    a = unix2datetime(1555430400)
    print(a)
