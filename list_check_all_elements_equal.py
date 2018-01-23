#coding=utf-8

'''

the file shows check the list elements all equal, all equal with the first element

'''

import unittest

def is_list_elements_equal(l):
    if not l :return True
    return all(l[0]== e for e in l)


def is_list_elements_equal_2(l):
    '''
    Condition: None not in list
    '''
    if not l: return True
    f = lambda x1,x2 : x1 if x1 == x2 else None
    r  = reduce(f,l)
    return r is not None


class MyTestCase(unittest.TestCase):

    def test1(self):
        data = [
            ([1, 1, 1, 1, 1],True),
            ([1, 2, 3, 1],False)
        ]

        for e,r in data:
            b1 = is_list_elements_equal(e)
            b2 = is_list_elements_equal_2(e)
            self.assertEqual(b1,r)
            self.assertEqual(b1,b2)


if __name__ == '__main__':
    unittest.main()