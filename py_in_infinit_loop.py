#coding=utf-8



import os
import sys

class MyClass(object):

    def __init__(self):
        self._v = {'a':1,
                   'b':2}


    def __getitem__(self, item):

        # startswith 0 , infinit loop

        print ('__getitem__ ({})'.format(item))

        return self._v.get(item,None)

def entry():

    o = MyClass()
    print ('1' in o)


if __name__ == '__main__':
    entry()