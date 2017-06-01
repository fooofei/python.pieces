#coding=utf-8


def result_show(r):

    for v in r:
        print ('{} {}'.format(v['name'], v['age']))


g_data = [
    {'name': 'Alen',
     'age': 13},
    {'name': 'Bob',
     'age': 67},

    {'name': 'ada',
     'age': 30},
    {'name': 'Alen',
     'age': 9},

    {'name': 'Bob',
     'age': 33},
    {'name': 'Alen',
     'age': 66},

    {'name': 'Bob',
     'age': 2},

    {'name': 'Bob',
     'age': 25},

    {'name': 'candy',
     'age': 5},

    {'name': 'Chiyan',
     'age': 8},
    {'name': 'Alen',
     'age': 10},

]


def sorted_key(data):
    data.sort(key=lambda x: x['name'])
    return data
    '''
    
    A is smaller than a
    
    Alen 13
    Alen 9
    Alen 66
    Alen 10
    Bob 67
    Bob 33
    Bob 2
    Bob 25
    Chiyan 8
    ada 30
    candy 5
    '''

def sorted_key_ignore_case(data):

    data.sort(key= lambda x : x['name'].lower())
    return data

    '''
    ada 30
    Alen 13
    Alen 9
    Alen 66
    Alen 10
    Bob 67
    Bob 33
    Bob 2
    Bob 25
    candy 5
    Chiyan 8
    '''


def sorted_multi_keys_error(data):
    '''
    someone say sort twice, the sample verify it not work

    such as https://stackoverflow.com/questions/11206884/how-to-write-python-sort-key-functions-for-descending-values

    '''

    data.sort(key=lambda x: x['name'])
    data.sort(key=lambda x: x['age'])

    # same with
    # x = sorted(sorted(data,key=lambda  x :x['name']),key= lambda y: y['age'])
    return data

    '''
    Bob 2
    candy 5
    Chiyan 8
    Alen 9
    Alen 10
    Alen 13
    Bob 25
    ada 30
    Bob 33
    Alen 66
    Bob 67
    '''

def sorted_multi_keys1(data):

    '''

    ref https://docs.python.org/2/howto/sorting.html#sortinghowto
     # The Old Way Using Decorate-Sort-Undecorate


    This idiom works because tuples are compared lexicographically; the first items are compared;
    if they are the same then the second items are compared, and so on.

    '''

    data.sort(key=lambda x : (x['name'],x['age']))

    return data
    '''
    Alen 9
    Alen 10
    Alen 13
    Alen 66
    Bob 2
    Bob 25
    Bob 33
    Bob 67
    Chiyan 8
    ada 30
    candy 5
    
    '''

def sorted_multi_keys2(data):

    from operator import itemgetter # obj['item']
    from operator import attrgetter # obj.attr
    from operator import methodcaller # obj.method()

    data.sort(key= itemgetter('name','age'))
    return data

    '''
    Alen 9
    Alen 10
    Alen 13
    Alen 66
    Bob 2
    Bob 25
    Bob 33
    Bob 67
    Chiyan 8
    ada 30
    candy 5

    '''

def sorted_multi_keys3(data):

    def _my_cmp(x,y):

        if x['name'] == y['name']:
            return cmp(x['age'],y['age'])

        return cmp(x['name'],y['name'])

    from functools import cmp_to_key

    data.sort(key=cmp_to_key(_my_cmp))
    return data

    '''
    Alen 9
    Alen 10
    Alen 13
    Alen 66
    Bob 2
    Bob 25
    Bob 33
    Bob 67
    Chiyan 8
    ada 30
    candy 5
    '''



def entry():
    from copy import deepcopy

    func = [
        sorted_key,
        sorted_key_ignore_case,
        sorted_multi_keys_error,
        sorted_multi_keys1,
        sorted_multi_keys2,
        sorted_multi_keys3,

    ]

    data = sorted_multi_keys2(deepcopy(g_data))

    result_show(data)


    assert (sorted_multi_keys1(deepcopy(g_data))
                               == sorted_multi_keys2(deepcopy(g_data))
                               == sorted_multi_keys3(deepcopy(g_data))
                               )


if __name__ == '__main__':
    entry()