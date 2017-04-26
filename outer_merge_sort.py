#coding=utf-8

import sys

def outer_merge_sort(sorted_streams):
    '''
    各个 stream 流有序，合并到一个大的 stream 中
    :return: generator
    '''
    import heapq
    return heapq.merge(*sorted_streams)



def entry():
    from cStringIO import StringIO

    content1 = '''\
1
4
5
6
'''
    content2 = '''\
2
3
5
7
9
'''

    f1 = StringIO(content1)
    f2 = StringIO(content2)
    r = outer_merge_sort([f1,f2])

    fr = StringIO()
    for e in r:
        fr.write(e)
    print (fr.getvalue())

    '''
    1
    2
    3
    4
    5
    5
    6
    7
    9
    '''

if __name__ == '__main__':
    entry()