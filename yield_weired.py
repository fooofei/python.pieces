#coding=utf-8


def foo1():
    print ('hello from {}'.format(foo1.__name__))


def foo2():
    print ('hello from {}'.format(foo2.__name__))

    if False:  # 没有运行的代码，也能把函数 foo2 变为 generator 
        yield 3

def entry():
    # foo1()  #hello from foo1
    f = foo2()  # nothing    foo2() is a generator

    print (next(f))

    '''
    hello from foo2
    Traceback (most recent call last):
      File "D:\src_git\py_pieces\weired_yeild.py", line 22, in <module>
        entry()
      File "D:\src_git\py_pieces\weired_yeild.py", line 18, in entry
        print (next(f))
    StopIteration
    '''


if __name__ == '__main__':
    entry()