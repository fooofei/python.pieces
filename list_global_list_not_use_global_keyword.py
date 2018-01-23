#coding=utf-8

'''
the file shows about modify a element of list
'''

# ref https://stackoverflow.com/questions/6329499/in-python-why-is-list-automatically-global
# ref https://stackoverflow.com/questions/4630543/defining-lists-as-global-variables-in-python

import unittest

list1 = [1,2,3]
list2 = [1,2,3]
list3 = [1,2,3]
list4 = [1,2,3]
list5 = [1,2,3]


class MyTestCase(unittest.TestCase):

    def assign_without_global(self):
        list1 = [4, 5, 6]

    def test_assign_without_global(self):
        self.assign_without_global()
        self.assertEqual(list1, [1,2,3])

    def assign_with_global(self):
        global list2
        list2=[4,5,6]
    def test_assign_with_global(self):
        self.assign_with_global()
        self.assertEqual(list2, [4,5,6])

    def method_call_without_global(self):
        list3.append(4)
    def test_method_call_without_global(self):
        self.method_call_without_global()
        self.assertEqual(list3, [1,2,3,4])

    def method_call_with_global(self):
        global list4
        list4.append(4)
    def test_method_call_with_global(self):
        self.method_call_with_global()
        self.assertEqual(list4, [1,2,3,4])

    def method_call_without_global2(self):
        list5[-1] = 9
    def test_method_call_without_global2(self):
        self.method_call_without_global2()
        self.assertEqual(list5, [1,2,9])



if __name__ == '__main__':
    unittest.main()