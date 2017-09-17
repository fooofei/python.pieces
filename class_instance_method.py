#coding=utf-8

'''
    Python 中给一个类添加方法的时候的书写形式有以下几种

    第一参数 self 的名字不是固定的
'''

import unittest

class Baby(object):

    def foo(self):
        print ('baby:foo()')
        print (self)
        return self

    def cry(*args):
        print ('baby:cry()')
        print (args)
        return args[0]

    def eat(x):
        print ('baby:eat()')
        print (x)
        return x


class MyTestCase(unittest.TestCase):
    def test1(self):
        obj = Baby()

        # all equals with self
        self.assertEqual(obj.foo(),obj.cry(),obj.eat())


'''
baby:foo()
<__main__.Baby object at 0x027B6BF0>

baby:cry()
(<__main__.Baby object at 0x027B6BF0>,)

baby:eat()
<__main__.Baby object at 0x027B6BF0>
'''

if __name__ == '__main__':
    unittest.main()