#coding=utf-8



import os
import sys

class MyClass1(object):

    def __init__(self):
        self._v = {'a':1,
                   'b':2}


class MyClass2(object):
    def __init__(self):
        self._v = {'a':1,
                   'b':2}


    def __getitem__(self, item):
        print ('call MyClass2:__getitem__({})'.format(item))
        return self._v.get(item,None)




def is_iterable_by_collections(obj):
    from collections import Iterable
    return isinstance(obj, Iterable)

def is_iterable_by_iter(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def iterable():

    o1 = MyClass1()
    o2 = MyClass2()

    print ('o1 Iterable {}'.format(is_iterable_by_collections(o1)))
    print ('o1 iter {}'.format(is_iterable_by_iter(o1)))

    print ('o2 Iterable {}'.format(is_iterable_by_collections(o2)))
    print ('o2 iter {}'.format(is_iterable_by_iter(o2)))

    '''
    o1 Iterable False
    o1 iter False
    o2 Iterable False
    o2 iter True
    '''

def iter_():

    o1 = MyClass1()

    '''
    # TypeError
    for e in o1:
        print (e)
    '''

    o2 = MyClass2()
    c = 0


    for e in o2:
        print (e)

        c += 1
        if c > 10:
            break

    '''
    call MyClass2:__getitem__(0)
    None
    call MyClass2:__getitem__(1)
    None
    call MyClass2:__getitem__(2)
    None
    call MyClass2:__getitem__(3)
    None
    call MyClass2:__getitem__(4)
    None
    call MyClass2:__getitem__(5)
    None
    call MyClass2:__getitem__(6)
    None
    call MyClass2:__getitem__(7)
    None
    call MyClass2:__getitem__(8)
    None
    call MyClass2:__getitem__(9)
    None
    call MyClass2:__getitem__(10)
    None
    '''

def error_infinit_loop():

    o2 = MyClass2()

    '1' in o2

if __name__ == '__main__':
    error_infinit_loop()