# coding=utf-8

'''

场景: 从服务端返回的数据是 json 格式，我们想要的数据要经过连续多次 dict.get。

'''

import os
import sys
import unittest


def dict_item_getter(data, keys):
    f = lambda x, y: x.get(y,None) if isinstance(x,dict)  else None
    return reduce(f, keys, data)


def dict_item_getter2(data, keys):
    for e in keys:
        if isinstance(data,dict):
            data = data.get(e,None)
        else: return None
    else:
        return data


class MyTestCase(unittest.TestCase):


    def test(self):

        data = {'1': {'2': {'3': 'hello'}}}
        keys = [
            (['1'],{'2': {'3': 'hello'}}),
            (['1', '2'], {'3': 'hello'}),
            (['1', '2', '3'],'hello'),
            (['1', '2', '3', '4'],None),
            (['1', '3'],None),
        ]

        for v in keys:

            self.assertEqual(v[1], dict_item_getter(data,v[0]))
            self.assertEqual(v[1], dict_item_getter2(data,v[0]))


if __name__ == '__main__':
    unittest.main()