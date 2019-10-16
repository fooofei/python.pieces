# coding=utf-8

'''
The main idea is to use dictionnaries instead of doubly-linked lists to represent the matrix.
We already have Y. From it, we can quickly access the columns in each row.
Now we still need to do the opposite,
namely a quick access from the columns to the rows.
For this, we can modify X by transforming it into a dictionnary.
In the above example, it would be written like this
'''


def solve(columns, rows, solution):
    if not columns:
        yield list(solution)
    else:
        c = min(columns, key=lambda c: len(columns[c]))
        for r in list(columns[c]):
            solution.append(r)
            cols = select(columns, rows, r)
            for s in solve(columns, rows, solution):
                yield s
            deselect(columns, rows, r, cols)
            solution.pop()


def select(columns, rows, r):
    cols = []
    for column_name in rows[r]:
        for row_name in columns[column_name]:
            for k in rows[row_name]:
                if k != column_name:
                    columns[k].remove(row_name)
        cols.append(columns.pop(column_name))
    return cols


def deselect(columns, rows, r, cols):
    for column_name in reversed(rows[r]):
        columns[column_name] = cols.pop()
        for row_name in columns[column_name]:
            for k in rows[row_name]:
                if k != column_name:
                    columns[k].add(row_name)


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
