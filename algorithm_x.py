#coding=utf-8

'''
The main idea is to use dictionnaries instead of doubly-linked lists to represent the matrix.
We already have Y. From it, we can quickly access the columns in each row.
Now we still need to do the opposite,
namely a quick access from the columns to the rows.
For this, we can modify X by transforming it into a dictionnary.
In the above example, it would be written like this
'''

def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

def main():
    X1 = {1, 2, 3, 4, 5, 6, 7}
    Y1 = {
        'A': [1, 4, 7],
        'B': [1, 4],
        'C': [4, 5, 7],
        'D': [3, 5, 6],
        'E': [2, 3, 6, 7],
        'F': [2, 7]}

    X = {j: set() for j in X1}
    for i in Y1:
        for j in Y1[i]:
            X[j].add(i)

    solution = []
    for i in solve(X,Y1, solution):
        print(f"answer= {i}")

    print(solution)

if __name__ == '__main__':
    main()