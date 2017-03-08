
#coding=utf-8

import random

def red_envelope_random(cents, people_number):
    '''
    - 红包前最低单位是分，是整数
    - 每人最低得到 1 分
    :param cents:
    :param people_number:
    :return:
    '''
    if not (isinstance(cents,int) and cents and people_number and cents>=people_number):
        raise ValueError('error')

    result_fix_base = [1]*people_number
    result_rand = []
    rand_cents = cents - 1 * people_number
    rest_cents = rand_cents

    rand_numbers = [random.uniform(10,100) for _ in range(people_number)]
    rand_sum = float(sum(rand_numbers))

    for inx in range(people_number):
        scale = rand_numbers[inx] / rand_sum
        o =  int(rand_cents*scale)
        result_rand.append(o)
        rest_cents -= o
    else:
        result_rand[-1] += rest_cents

    result = [ a+b for a, b in zip(result_fix_base,result_rand)]
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