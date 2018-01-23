# coding=utf-8

'''
the file shows how to print a json which contains chinese
'''

import json


def entry():
    value = {
        'code': '1',
        'msg': u'测试abc'
    }

    print (value)
    # {'msg': u'\u6d4b\u8bd5abc', 'code': '1'}

    print (json.dumps(value, ensure_ascii=False, encoding='utf-8'))
    # {"msg": "测试abc", "code": "1"}


if __name__ == '__main__':
    entry()
