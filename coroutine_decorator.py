#coding=utf-8
'''

Someone use this decorator of  coroutine to wrap a function,

to auto start a generator.

I found by this way, it lost it's first yield return value.

https://books.google.com.tw/books?id=kYZHCgAAQBAJ&pg=PA486&lpg=PA486&dq=using+a+decorator++remembering+to+call+.next()+is+easy+to+forget&source=bl&ots=irDlZyELKn&sig=wdr4hzxG4PgVPYgJAefVvPfCIj0&hl=zh-CN&sa=X&ved=0ahUKEwi0kKnCnurUAhVNNbwKHcOxDZUQ6AEIITAA#v=onepage&q=using%20a%20decorator%20%20remembering%20to%20call%20.next()%20is%20easy%20to%20forget&f=false


'''

import os
import sys
import unittest

def coroutine(func):

    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr

    return start


def foo_no_decorator():

    for i in range(1,4):
        print('before yield with i={}'.format(i))
        y = yield i
        print('after yield with i={} y={}'.format(i,y))


@coroutine
def foo_use_decorator():
    for i in range(1, 4):
        print('before yield with i={}'.format(i))
        y = yield i
        print('after yield with i={} y={}'.format(i, y))


class MyTestCase(unittest.TestCase):

    def test_no_decorator(self):
        no_decorator = foo_no_decorator()

        self.assertEqual(1, no_decorator.send(None))
        self.assertEqual(2, no_decorator.send(11))
        self.assertEqual(3, no_decorator.send(22))

        with self.assertRaises(StopIteration):
            no_decorator.send(33)


    def test_use_decorator(self):
        '''
        !!! NOTICE
        Compare the test_no_decorator(), we can see, we lost the
        first yield <value>.

        '''

        use_decorator = foo_use_decorator()

        self.assertEqual(2, use_decorator.send(11))
        self.assertEqual(3, use_decorator.send(22))

        with self.assertRaises(StopIteration):
            use_decorator.send(33)




if __name__ == '__main__':
    unittest.main()