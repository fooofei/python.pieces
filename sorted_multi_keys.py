#coding=utf-8


def result_show(r):

    print '['

    for e in r:
        print ('{},'.format(e))

    print ']'


import os
import sys
import unittest


g_data = [
    {'age': 7, 'name': 'b'},
    {'age': 3, 'name': 'a'},
    {'age': 5, 'name': 'b'},
    {'age': 8, 'name': 'c'},
    {'age': 9, 'name': 'b'},
    {'age': 2, 'name': 'A'},
]


g_data_sorted_by_name = [
    {'age': 2, 'name': 'A'},
    {'age': 3, 'name': 'a'},
    {'age': 7, 'name': 'b'},
    {'age': 5, 'name': 'b'},
    {'age': 9, 'name': 'b'},
    {'age': 8, 'name': 'c'}
]

g_data_sorted_by_name_ignore_case = [
    {'age': 3, 'name': 'a'},
    {'age': 2, 'name': 'A'},
    {'age': 7, 'name': 'b'},
    {'age': 5, 'name': 'b'},
    {'age': 9, 'name': 'b'},
    {'age': 8, 'name': 'c'},
]

# name 优先  ，name 相等后 依据 age 排序
g_data_sorted_by_name_age=[
    {'age': 2, 'name': 'A'},
    {'age': 3, 'name': 'a'},
    {'age': 5, 'name': 'b'},
    {'age': 7, 'name': 'b'},
    {'age': 9, 'name': 'b'},
    {'age': 8, 'name': 'c'},
]







class MyTestCase(unittest.TestCase):

    def test_sorted_by_key_name(self):

        l = sorted(g_data, key=lambda v:v['name'])

        self.assertEqual(l, g_data_sorted_by_name)

    def test_sorted_by_key_name_ignore_case(self):
        l = sorted(g_data, key=lambda v:v['name'].lower())

        self.assertEqual(l, g_data_sorted_by_name_ignore_case)


    def test_sorted_by_key_name_age(self):
        '''
        someone say sort twice, the sample verify it not work
        such as https://stackoverflow.com/questions/11206884/how-to-write-python-sort-key-functions-for-descending-values

        error:
            data.sort(key=lambda x: x['name'])
            data.sort(key=lambda x: x['age'])

        ref https://docs.python.org/2/howto/sorting.html#sortinghowto
        # The Old Way Using Decorate-Sort-Undecorate


        This idiom works because tuples are compared lexicographically; the first items are compared;
        if they are the same then the second items are compared, and so on.


        '''


        l = sorted(g_data, key=lambda x : (x['name'],x['age']))

        self.assertEqual(l, g_data_sorted_by_name_age)

    def test_sorted_by_key_name_age2(self):
        from operator import itemgetter  # obj['item']
        from operator import attrgetter  # obj.attr
        from operator import methodcaller  # obj.method()

        l = sorted(g_data, key=itemgetter('name', 'age'))

        self.assertEqual(l, g_data_sorted_by_name_age)


    def test_sorted_by_key_name_age3(self):
        def _my_cmp(x, y):
            if x['name'] == y['name']:
                return cmp(x['age'], y['age'])

            return cmp(x['name'], y['name'])

        from functools import cmp_to_key

        l = sorted(g_data, key=cmp_to_key(_my_cmp))
        self.assertEqual(l, g_data_sorted_by_name_age)

if __name__ == '__main__':
    unittest.main()