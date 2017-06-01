#coding=utf-8


# ref https://stackoverflow.com/questions/6329499/in-python-why-is-list-automatically-global
# ref https://stackoverflow.com/questions/4630543/defining-lists-as-global-variables-in-python


list1 = [1,2,3]
list2 = [1,2,3]
list3 = [1,2,3]
list4 = [1,2,3]
list5 = [1,2,3]


def assignment_without_global():

    list1 = [4,5,6]

def assignment_with_global():
    global list2
    list2 = [4,5,6]


def method_call_without_global():

    list3.append(4)


def method_call_with_global():
    global list4
    list4.append(4)


def method_call2_without_global():
    global list5
    list5[-1] = 9


def entry():

    assignment_without_global()
    print (list1)  # [1, 2, 3]

    assignment_with_global()
    print (list2) # [4, 5, 6]


    method_call_without_global()
    print (list3) # [1, 2, 3, 4]

    method_call_with_global()
    print (list4) # [1, 2, 3, 4]


    method_call2_without_global()
    print (list5) # [1, 2, 9]


if __name__ == '__main__':
    entry()