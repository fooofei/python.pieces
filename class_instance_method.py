#coding=utf-8

'''
    Python 中给一个类添加方法的时候的书写形式有以下几种
'''

class Baby(object):

    def foo(self):
        print ('baby:foo()')
        print (self)

    def cry(*args):
        print ('baby:cry()')
        print (args)

    def eat(x):
        print ('baby:eat()')
        print (x)


def entry():
    a = Baby()
    a.foo()
    print ('')

    a.cry()
    print ('')

    a.eat()
    print ('')


'''
baby:foo()
<__main__.Baby object at 0x027B6BF0>

baby:cry()
(<__main__.Baby object at 0x027B6BF0>,)

baby:eat()
<__main__.Baby object at 0x027B6BF0>
'''

if __name__ == '__main__':
    entry()