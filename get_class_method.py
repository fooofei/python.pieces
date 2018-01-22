#coding=utf-8

import os
import sys

def get_class_methods(klass):
  ''' :return all callable methods by user defined '''
  ret = dir(klass)
  if hasattr(klass, '__bases__'):
    for base in klass.__bases__:
      ret = ret + get_class_methods(base)

  ret = filter(lambda m: not m.startswith('_'), ret)
  o = klass()
  return filter(lambda v: callable(getattr(o, v)), ret)


class test(object):
  def __init__(self):
    print('test_init')

  def foo1(self):
    print('test_foo1')

  def foo2(self):
    print('test_foo2')

def entry():
  methods = get_class_methods(test)
  print(len(methods))
  print(methods) # ['foo1', 'foo2']  not include __init__()

  ins = test() # print __init__()
  for m in methods:
    getattr(ins,m)() # call foo1() and foo2()

if __name__ == '__main__':
    entry()
