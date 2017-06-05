#coding=utf-8



def foo1():

    l = [1,2,3,4,5]

    l2 = [v*v for v in l]

    print (l2) # [1, 4, 9, 16, 25]


def foo2():
    l = [1,2,3,4,5]

    l2 = (v*v for v in l)

    print (l2) # <generator object <genexpr> at 0x0273F620>


    print (list(l2)) # [1, 4, 9, 16, 25]



if __name__ == '__main__':
    foo1()
    foo2()