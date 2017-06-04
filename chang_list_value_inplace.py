# coding=utf-8


def foo1(l):
    l = sorted(l)


def foo2(l):
    l[::] = sorted(l)


def entry():
    from copy import deepcopy
    l1 = ['b', 'a', 'c', 'f', 'e', 'd']
    l2 = deepcopy(l1)

    foo1(l1)
    print (l1)  # ['b', 'a', 'c', 'f', 'e', 'd']

    foo2(l2)
    print (l2)  # ['a', 'b', 'c', 'd', 'e', 'f']


if __name__ == '__main__':
    entry()
