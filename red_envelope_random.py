#coding=utf-8

import random

def red_envelope_random(cents, people_number):
    '''
    - ref http://www.letiantian.me/2016-04-23-red-envelope/
    - 红包前最低单位是分，是整数
    - 每人最低得到 1 分
    :param cents:
    :param people_number:
    :return:
    '''
    if not (isinstance(cents,int) and cents and people_number and cents>=people_number):
        raise ValueError('error')

    # 先给每人发 1 分保底
    result_fix_base = [1]*people_number
    result_rand = []
    rand_cents = cents - 1 * people_number
    rest_cents = rand_cents

    # 得到一组随机数
    rand_numbers = [random.uniform(10,100) for _ in range(people_number)]
    rand_sum = float(sum(rand_numbers))

    # 按照随机数的占比 给每个人发钱
    for inx in range(people_number):
        scale = rand_numbers[inx] / rand_sum
        o =  int(rand_cents*scale)
        result_rand.append(o)
        rest_cents -= o
    else:
        # 最后一个把因为 float 靠下取整余下的钱都拿了
        result_rand[-1] += rest_cents

    # 固定钱 + 随机钱
    result = [ a+b for a, b in zip(result_fix_base,result_rand)]

    # 打乱顺序
    random.shuffle(result)

    assert sum(result) == cents
    assert  len(result) == people_number

    return  result


def unit_test_red_envelope_random():
    print (red_envelope_random(9,3))
    print (red_envelope_random(99,3))
    print (red_envelope_random(99,33))
    print (red_envelope_random(100,10))


if __name__ == '__main__':
    unit_test_red_envelope_random()