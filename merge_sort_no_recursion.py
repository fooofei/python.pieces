#coding=utf-8

'''

合并思路来自 http://www.voidcn.com/blog/dreamhougf/article/p-3900053.html

非递归的归并排序（Merge Sort）使用迭代的思想，将递归方式改变成自底向上的思想进行排序。
归并排序的原理同样是将一个无序的N个元素序列划分成N个有序子序列，然后再两两合并，
然后再将合并后的N/2（或者N/2 + 1）个子序列继续进行两两合并，以此类推得到一个完整的有序序列。
不同点在于递归的时候我们需要先用递归的方式将原始序列划分成单个的子序列在进行合并，
而非递归迭代的时候我们需要采用不同的步长对子序列的个数进行控制。

'''

def merge(arr,temp, left, mid, right):
    '''
    left mid right 是 arr 中的索引
    把 arr 中 [left,mid) [mid,right) 两组合并到 temp 中
    '''

    i = left
    j = mid

    while i<mid and j < right:
        if arr[i]<=arr[j]:
            temp.append(arr[i])
            i+=1
        else:
            temp.append(arr[j])
            j+=1

    for e in range(i,mid):
        temp.append(arr[e])
    for e in range(j,right):
        temp.append(arr[e])


def merge_pass(arr, step):
    '''
    按照 [0,step) [step,2*step)  的组织方式，依次
       合并组：
       [0,step) [step,step+step=2*step) 
       [2*step, 2*step+step= 3*step) [3*step, 3*step+step= 4step)
        ... 
    '''
    i=0
    temp=[]
    while i+2*step < len(arr):
        merge(arr,temp,i,i+step,i+2*step)
        i += 2*step

    # 不够按照 step 分两组
    if i+step<len(arr):
        merge(arr,temp,i,i+step,len(arr))
    else:
        for e in range(i,len(arr)):
            temp.append(arr[e])

    for e in range(0,len(temp)):
        arr[e] = temp[e]


def merge_sort_no_recursion(arr):
    step = 1
    while step < len(arr):
        merge_pass(arr,step)
        step *= 2


def test(ar):
    print ('before:{}'.format(ar))
    merge_sort_no_recursion(ar)
    assert (sorted(ar)==ar)
    print ('  after:{}'.format(ar))


def entry():
    test([2,1])
    test([2,3,1])
    test([1, 5, 7, 4, 3, 2, 1, 9, 0, 10, 43, 64])


if __name__ == '__main__':
    entry()