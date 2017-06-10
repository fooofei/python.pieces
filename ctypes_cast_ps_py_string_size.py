#coding=utf-8

'''
 We have two ways to get internal buffer of the bytes string( not the unicode string).

 1 use ctypes.cast

 2 use pythonapi PyString_AsStringAndSize, export from python c module


'''


import ctypes



def ctypes_cast_c_void_p(v): return ctypes.cast(v, ctypes.c_void_p)
def bytes_string_address(v): return ctypes_cast_c_void_p(v)

def bytes_string_address2(v):
    Py_ssize_t = ctypes.c_uint
    f = ctypes.pythonapi.PyString_AsStringAndSize
    f.restype = ctypes.c_int
    f.argtypes = [ctypes.py_object,
                                      ctypes.POINTER(ctypes.c_char_p),
                                      ctypes.POINTER(Py_ssize_t)]

    addr = ctypes.c_char_p()
    size = Py_ssize_t()
    hr = f(v, ctypes.pointer(addr),ctypes.pointer(size))
    assert (hr==0)
    return ctypes_cast_c_void_p(addr)



def entry():
    from ctypes import string_at

    v = 'helloworld'

    addr1 = bytes_string_address(v)
    addr2 = bytes_string_address2(v)

    assert (addr1.value == addr2.value)


    assert (v
            == string_at(addr1.value,len(v))
            == string_at(addr2.value,len(v)))


    print ('pass all')



if __name__ == '__main__':
    entry()