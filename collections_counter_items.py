#coding=utf-8

'''

    Python 中计数的方式
    
    如果不使用 collections.Counter 的话，会是这么用 counter_list_old_way()

'''

def counter_list():
    from collections import Counter
    a = ['a','a','b','b',
         'c','c','c']

    b = Counter(a)
    print (b.items())
    '''
    [('a', 2), ('c', 3), ('b', 2)]
    '''


def counter_list2():
    from collections import Counter

    a = ['a', 'a', 'b', 'b',
         'c', 'c', 'c']
    b = Counter()

    for e in a:
        b.update({e:1})
    print (b.items())

    '''
    [('a', 2), ('c', 3), ('b', 2)]
    '''

def counter_update_items():
    from collections import Counter

    b = Counter()

    b.update({'a':4})
    b.update({'a':7})
    b.update({'b':2})
    b.update({'b':2})
    b.update({'c':1})
    b.update({'c':0})

    print (b.items())
    '''
    [('a', 11), ('c', 1), ('b', 4)]
    '''

def counter_update_items2():
    from collections import Counter

    b = Counter()


    b.update({'a':'4'}) # 首次使用时 b 为空 'a' 直接使用 dict 的构造方式(update())填充进去 值为 '4'
    b.update({'a':'7'}) # 取出 'a' 的值 '4' 在此基础上 + '7'， 为 '47'

    # b.update({'b':'1'}) # error  # b 不为空，使用dict 的 get(val,default=0) 的方式 + '1' ， 出现 0 + '1' 导致异常

    '''
     same use
     
    b.update(a='4')
    b.update(a='7')
    b.update(b='1')
    
    '''

    print (b.items())

    '''
    [('a', '47')]
    
    '''

def counter_list_old_way():
    a = ['a', 'a', 'b', 'b',
         'c', 'c', 'c']

    b = {}

    for e in a :
        if not e in b:
            b[e] = 1
        else:
            b[e] += 1

    print (b.items())


def entry():
    counter_list()
    counter_list2()
    counter_update_items()
    counter_update_items2()
    counter_list_old_way()

if __name__ == '__main__':
    entry()