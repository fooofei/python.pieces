#coding=utf-8

import os
import logging


class LoggerHelper(object):
    datefmt = u'%Y/%m/%d %H:%M:%S'

    def __init__(self, fmt=None):
        self._log = None
        self._memory_handler = None
        self._format = fmt if fmt else u'[%(asctime)s module=%(module)s func=%(funcName)s %(levelname)s] %(message)s'

    def _get_formatter(self):
        return logging.Formatter(self._format,datefmt=LoggerHelper.datefmt)

    def get_logger(self):

        if self._log is None:
            handler = logging.StreamHandler()
            handler.setFormatter(self._get_formatter())
            log = logging.getLogger(__name__)
            while log.handlers: log.handlers.pop()  # 遇到过重复输出
            log.addHandler(handler)
            log.setLevel(logging.DEBUG)
            self._log = log
        return self._log

    def enable_memory_log(self):
        from logging.handlers import MemoryHandler
        if self._memory_handler is None:
            h = MemoryHandler(10 * 1024 * 1024)
            h.setFormatter(self._get_formatter())
            self._log.addHandler(h)
            self._memory_handler = h

    def get_formated_messages(self):
        '''
        log 输出到屏幕的同时 可以内存留一份 方便程序结束发邮件 汇总信息
        '''
        if not self._memory_handler: return []
        return (self._memory_handler.format(rec) for rec in self._memory_handler.buffer)


def get_logger_2():
    '''
    other module logging also output
    '''
    # >= level will be output
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__) # __main__
    return log

log_helper = LoggerHelper()
log = log_helper.get_logger()





def foo1():
    log.info(u'logger info foo1()')
    log.debug(u'logger debug foo1()')
    log.warn(u'logger warn foo1()')
    log.error(u'logger error foo1()')
    print ('call foo1()')



def entry():

    log_helper.enable_memory_log()

    log.info(u'logger info entry()')
    log.debug(u'logger debug entry()')
    print ('call entry()')
    foo1()

    print (u'dup log messages ->')

    print(u'\n'.join(list(log_helper.get_formated_messages())))


if __name__ == '__main__':
    entry()