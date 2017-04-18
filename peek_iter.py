#coding=utf-8


def peek_iter(iter_ins):
    '''
    iter_ins.next() 会把值取出来，该函数取值后，再拼装回去，做到窥探的目的
    :param iter_ins:  iterable, such as iter([1,2,3])
    :return:  
    '''
    import itertools
    r = iter_ins.next()
    iter_ins = itertools.chain([r],iter_ins)
    return iter_ins,r


def entry():
    a = [1,2,3]
    a = iter(a)

    a,value = peek_iter(a)
    print (value)

    a, value = peek_iter(a)
    print (value)

    a, value = peek_iter(a)
    print (value)

    '''
    1
    1
    1
    '''

if __name__ == '__main__':
    entry()

