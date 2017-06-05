#coding=utf-8

'''

    use itertools.tee to copy an generator

    1 生成两个 generator 但是实例并没有增加
    2 两个 generator 持有同一份实例的引用 在一个 generator 中修改了一个实例 另一个 generator 也会受到修改影响
    3 官方警告使用 itertools.tee 分裂之后 母 generator 不再使用 https://docs.python.org/2/library/itertools.html
    4 官方建议 如果其中 1 个 iterator 走的太快 其他的 iterator 没走 使用 list() 比 tee() 更快
'''

import itertools
import sys

count = 0

class Instance(object):
    def __init__(self, v):
        global count
        print ('instance init {}'.format(count))
        count += 1
        self._v = v

    @property
    def v(self):
        return self._v

    def __del__(self):
        print ('instance del')

    def __str__(self):
        return super(Instance,self).__str__()

    def __repr__(self):
        return  '{}'.format(self.v)

def entry():

    a = [Instance(i) for i in range(10)]

    ai = iter(a)

    ai1,ai2  = itertools.tee(ai)

    print(list(ai1))
    print(list(ai))

    for v in ai1:
        if v.v == 5:
            v._v = 55
        sys.stdout.write('{} '.format(v))
    print('')

    print(list(ai2))  # 受到 上面的修改影响  5 变为 55

if __name__ == '__main__':
    entry()
