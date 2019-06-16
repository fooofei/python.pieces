#coding=utf-8

'''
处理多线程时 想在多个线程共享的变量中 atomic add 一个计数

itertools.count 是线程安全的计数 可以这样使用

'''



import itertools


class WithCurrent(object):
    '''
    为了方便查看 iterable 对象的 current 值
    '''
    def __init__(self, generator):
        self.__gen = iter(generator)

    def __iter__(self):
        return self

    def n_next(self):
        self.current = next(self.__gen)
        return self.current

    def __next__(self):
        return self.n_next()

    def next(self):
        return self.n_next()

    def __call__(self):
        return self

class ThreadSafeStat(object):

    def __init__(self):
        self.count = WithCurrent(itertools.count())

    def atomic_add_count(self):
        self.count.next()

