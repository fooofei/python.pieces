#coding=utf-8

'''
    我们见过的 reduce 的使用教程，都在计算几个数字的叠乘，如：
    r = reduce(lambda x,y : x* y, [1,2,3,4]) 
    # output : 24
    
    还可以可以用 reduce 重构多个 if 存在的代码

'''

from functools import reduce as reduce


def func_raw(var):
    if var :
        var = func1(var)
        if var :
            var = func2(var)
            if var :
                return func3(var)
    return None

def func_refactoring_code(var):
    _fn = lambda x, y: y(x) if x else None
    return(reduce(_fn, [var, func1, func2, func3]))


def _one_call(start_num):
    v = func_refactoring_code(start_num)
    print('result :{}'.format(v))
    assert (v == func_raw(start_num))


def func1(a):
    print('call {}'.format(func1.__name__))
    if a < 3:
        return None
    return a+1

def func2(a):
    print('call {}'.format(func2.__name__))
    if a <7:
        return None
    return a+2

def func3(a):
    print('call {}'.format(func3.__name__))
    if a < 10:
        return None
    return a+3


def entry():
    from functools import reduce

    print('begin 1 --------')
    _one_call(1)
    print('\n\nbegin 3 --------')
    _one_call(3)
    print('\n\nbegin 4 --------')
    _one_call(4)

    print('\n\nbegin 10 --------')
    _one_call(10)

if __name__ == '__main__':
    entry()

'''
begin 1 --------              
call func1                    
result :None                  
call func1                    
                              
                              
begin 3 --------              
call func1                    
call func2                    
result :None                  
call func1                    
call func2                    
                              
                              
begin 4 --------              
call func1                    
call func2                    
result :None                  
call func1                    
call func2                    
                              
                              
begin 10 --------             
call func1                    
call func2                    
call func3                    
result :16                    
call func1                    
call func2                    
call func3                    
                              
'''