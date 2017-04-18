#coding=utf-8


def foo():
    print ('enter...')
    a = yield 5
    print (a)

def entry():
    f = foo() # f is a generator
    print (next(f))   # next(f)  equal  f.send(None)

    print (f.send("from send"))  # 遇到下一个 yield 停止，如果不再有 yield ，那么抛出异常 StopIteration

    '''
    enter...
    5
    from send
    Traceback (most recent call last):
      File "D:\src_git\py_pieces\normal_yield.py", line 17, in <module>
        entry()
      File "D:\src_git\py_pieces\normal_yield.py", line 13, in entry
        print (f.send("from send"))
    StopIteration
    '''

if __name__ == '__main__':
    entry()