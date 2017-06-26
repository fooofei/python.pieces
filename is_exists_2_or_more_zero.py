#coding=utf-8

'''
几个同事工作之余的讨论问题

'''

import unittest

def is_exists_2_or_more_zero(a,b,c):
    '''
    3 个数字中 是否存在 2 个及以上的数为 0    
    :return: 
    '''
    return (a+b+c +1) == ((a+1)*(b+1)*(c+1))


class MyTestCase(unittest.TestCase):

    def test(self):
        cases = [
            ((0, 0, 0),True),
            ((0, 0, 1),True),
            ((0, 1, 0),True),
            ((1, 1, 0),False),
            ((0, 1, 1),False),
            ((1, 1, 1),False),
        ]

        for e in cases:
            self.assertEqual(is_exists_2_or_more_zero(*e[0]),e[1])



if __name__ == '__main__':
    unittest.main()