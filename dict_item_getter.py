# coding=utf-8



def dict_item_getter(data, keys):
    f = lambda x, y: x[y] if x and y in x else None
    return reduce(f, keys, data)


def dict_item_getter2(data, keys):
    for e in keys:
        if e in data:
            data = data[e]
        else:
            return None
    else:
        return data


def test(data, keys, func):
    print ('func {}'.format(func.__name__))
    print ('keys:{} result:{}'.format(keys, func(data, keys)))


def test2(data, keys):
    print('data {}'.format(data))
    for e in keys:
        print('-----------------------')
        test(data, e, dict_item_getter)
        test(data, e, dict_item_getter2)


def entry():
    a = {'1': {'2': {'3': 'hello'}}}
    a_keyss = [
        ['1'],
        ['1', '2'],
        ['1', '2', '3'],
        ['1', '2', '3', '4'],
        ['1', '3'],
    ]

    test2(a, a_keyss)


if __name__ == '__main__':
    entry()

'''
data {'1': {'2': {'3': 'hello'}}}
-----------------------
func dict_item_getter
keys:['1'] result:{'2': {'3': 'hello'}}
func dict_item_getter2
keys:['1'] result:{'2': {'3': 'hello'}}
-----------------------
func dict_item_getter
keys:['1', '2'] result:{'3': 'hello'}
func dict_item_getter2
keys:['1', '2'] result:{'3': 'hello'}
-----------------------
func dict_item_getter
keys:['1', '2', '3'] result:hello
func dict_item_getter2
keys:['1', '2', '3'] result:hello
-----------------------
func dict_item_getter
keys:['1', '2', '3', '4'] result:None
func dict_item_getter2
keys:['1', '2', '3', '4'] result:None
-----------------------
func dict_item_getter
keys:['1', '3'] result:None
func dict_item_getter2
keys:['1', '3'] result:None
'''