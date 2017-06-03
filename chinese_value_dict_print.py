#coding=utf-8




def entry():
    import json

    value = {
        'code':'1',
        'msg':u'测试abc'
    }


    print (value) # {'msg': u'\u6d4b\u8bd5abc', 'code': '1'}

    print (json.dumps(value,ensure_ascii=False, encoding='utf-8')) # {"msg": "测试abc", "code": "1"}

if __name__ == '__main__':
    entry()