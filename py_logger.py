#coding=utf-8

import os
import logging


def get_logger_1():
    FORMAT = u'%(asctime)s %(module)s %(funcName)s %(levelname)-8s %(message)s'
    datefmt = u'%Y/%m/%d %H:%M:%S'
    formatter = logging.Formatter(FORMAT,datefmt=datefmt)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log = logging.getLogger(__name__)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    return log


def get_logger_2():
    '''
    other module logging also output
    '''
    FORMAT = u'%(asctime)s %(module)s %(funcName)s %(levelname)-8s %(message)s'
    datefmt = u'%Y/%m/%d %H:%M:%S'
    # >= level will be output
    logging.basicConfig(format=FORMAT,level=logging.DEBUG,datefmt=datefmt)
    log = logging.getLogger(__name__) # __main__
    return log

log = get_logger_2()






def foo1():
    log.info(u'logger info foo1()')
    log.debug(u'logger debug foo1()')
    log.warn(u'logger warn foo1()')
    log.error(u'logger error foo1()')
    print ('call foo1()')

def entry():
    log.info(u'logger info entry()')
    log.debug(u'logger debug entry()')
    print ('call entry()')
    foo1()

if __name__ == '__main__':
    entry()