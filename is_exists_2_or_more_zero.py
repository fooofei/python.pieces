#coding=utf-8


def is_exists_2_or_more_zero(a,b,c):
    '''
    3 个数字中 是否存在 2 个及以上的数为 0    
    :return: 
    '''
    return (a+b+c +1) == ((a+1)*(b+1)*(c+1))


def entry():
    cases = [
        (0,0,0),
        (0,0,1),
        (0,1,0),
        (1,1,0),
        (0,1,1),
        (1,1,1)
    ]

    for e in cases:
        print (is_exists_2_or_more_zero(*e))

    '''
    True
    True
    True
    False
    False
    False
    '''

if __name__ == '__main__':
    entry()