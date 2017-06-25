#coding=utf-8

'''
One instance need to init, use, and close here.

Compare three ways to do this.

'''

from contextlib import contextmanager

class Instance(object):

    def cry(self):
        print ('call Instance:cry()')

    def release(self):
        pass

def create_instance():
    print ('call create_instance()')
    return Instance()

def free_instance(ins):
    print ('call free_instance()')
    ins.release()



def normal_way():

    ins = create_instance()

    # use instance to do work
    ins.cry()

    free_instance(ins)


def class_way():
    class _open_wrapper(object):

        def __init__(self):
            self._ins = create_instance()

        def __enter__(self):
            return self._ins

        def __exit__(self, exc_type, exc_val, exc_tb):
            free_instance(self._ins)

    with _open_wrapper() as i:
        i.cry()


@contextmanager
def _open_instance():
    ins = create_instance()
    try:
        yield ins
    finally:
        free_instance(ins)

def contextmanager_way():
    with _open_instance() as i:
        i.cry()



def entry():
    print ('normal way')
    normal_way()
    print ('\n\n')

    print ('class way')
    class_way()
    print ('\n\n')

    print ('contextmanager way <recommend>')
    contextmanager_way()
    print ('\n\n')

    '''
    normal way
    call create_instance()
    call Instance:cry()
    call free_instance()
    
    
    
    class way
    call create_instance()
    call Instance:cry()
    call free_instance()
    
    
    
    contextmanager way <recommend>
    call create_instance()
    call Instance:cry()
    call free_instance()
    '''


if __name__ == '__main__':
    entry()

