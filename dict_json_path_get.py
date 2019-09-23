#coding=utf-8

'''
这个文件演示如何通过 path 的形式访问一个 dict/json
'''

import os
import sys
import jsonpath_rw


def path1():
    from jsonpath_rw import jsonpath
    from jsonpath_rw import parse
    expr = parse("foo[*].baz")
    data = {
        "foo":[
            {"baz":1},
            {"baz":2}
        ]
    }
    target = expr.find(data)
    print(type(target))
    for match in target:
        print(match)




if __name__ == '__main__':
    path1()
