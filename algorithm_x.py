# coding=utf-8

'''
https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html

这个文件代码是用来演示精确覆盖问题的解
这个 Python 版本的实现，通过 dict 技巧来避免了十字链表的使用

作者是这样说的
The main idea is to use dictionnaries instead of doubly-linked lists to represent the matrix.
We already have Y. From it, we can quickly access the columns in each row.
Now we still need to do the opposite,
namely a quick access from the columns to the rows.
For this, we can modify X by transforming it into a dictionnary.
In the above example, it would be written like this
'''

from copy import deepcopy
import itertools


def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            removed_cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, removed_cols)
            solution.pop()


'''
select 实现的功能是当选择一个行时（即参数变量 r）
 
第一从 X 删除所有与这个行冲突的行
第二从 X 删除这个行中包含的列
Y 保持不变

# 一个错误的实现
def cover(X, Y, r):
    # 如果是我的话 我怎么写
    delete_cols = {}
    for column_name in Y[r]:
        bak_rows = deepcopy(X[column_name])
        for row_name in bak_rows:
            for k in Y[row_name]:
                X[k].remove(row_name)
        # 删除了这一列
        delete_cols.update({column_name: X.pop(column_name)})
    return delete_cols
'''


def select(X, Y, r):
    cols = []
    for column_name in Y[r]:
        for row_name in X[column_name]:
            for k in Y[row_name]:
                if k != column_name:
                    X[k].remove(row_name)
        cols.append(X.pop(column_name))
    return cols


def deselect(X, Y, r, cols):
    for column_name in reversed(Y[r]):
        X[column_name] = cols.pop()
        for row_name in X[column_name]:
            for k in Y[row_name]:
                if k != column_name:
                    X[k].add(row_name)


def main():
    cols = {1, 2, 3, 4, 5, 6, 7}
    rows = {
        'A': [1, 4, 7],
        'B': [1, 4],
        'C': [4, 5, 7],
        'D': [3, 5, 6],
        'E': [2, 3, 6, 7],
        'F': [2, 7]}

    X = {j: set() for j in cols}
    for row_name, subsets in rows.items():
        for col_name in subsets:
            X[col_name].add(row_name)

    solution = []
    for i in solve(X, rows, solution):
        print(f"answer= {i}")

    print(solution)


if __name__ == '__main__':
    main()
