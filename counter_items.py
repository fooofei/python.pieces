#coding=utf-8


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

def entry():
    counter_list()
    counter_list2()
    counter_update_items()

if __name__ == '__main__':
    entry()