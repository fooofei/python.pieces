#!/usr/bin/env python2.6
#coding=utf-8

'''
这个文件是用来同步本机的文件。
从一个目录（A）同步到另一个目录(B)。
目录 A 是通过 Samba 访问到另一个机器的目录。
目录 B 是本地目录。

使用这个技术来解决 IT 云主机 Samba 目录访问速度慢，无法在 Windows 编辑代码的问题.

缺陷是无法监控 mount 的 Samba 目录。

只能加 rsync 来实现文件复制。

还没加 rsync

'''

import os
import sys
import pyinotify # pip install pyinotify,  this module only support linux
import asyncore
import subprocess
import unittest
import time

from pyinotify import IN_DELETE
from pyinotify import IN_CREATE
from pyinotify import IN_MODIFY
from pyinotify import IN_CLOSE_WRITE
from pyinotify import ProcessEvent
from pyinotify import Notifier
from pyinotify import AsyncNotifier
from pyinotify import ExcludeFilter


class Processes(object):
  '''
  不断的添加运行的命令， 通过 aging 老化执行结束的进程句柄
  不阻塞主线程
  '''

  def __init__(self):
    self._q=[]

  def push(self, *args, **kwargs):
    p = subprocess.Popen(*args, **kwargs)
    self._q.append(p)

  def aging(self):
    self._q[:] = [e for e in self._q if e.poll() is None]

  def __len__(self):
    return len(self._q)

  def wait(self):

    for e in self._q:
      while e.poll() is None:
        e.wait()


class EventHandler(ProcessEvent):

  def __init__(self):
    self._sync = Sync()

  def process_IN_CREATE(self, event):
    #print('IN_CREATE {pn} {n}'.format(pn=event.pathname, n=event.name))
    pass

  def process_IN_DELETE(self, event):
    #print('IN_DELETE {n}'.format(n=event.pathname))
    self._sync.sync(event.pathname)

  def process_IN_MODIFY(self, event):
    #print('IN_MODIFY {n}'.format(n=event.pathname))
    pass

  def process_IN_CLOSE_WRITE(self, event):
    # write file finish
    # n=event.name is only the file name
    print(u'你正在关闭写文件 {pn}'.format(pn=event.pathname))
    self._sync.sync(event.pathname)

class Sync(object):
  '''
  只同步单个目录  兼顾 Config
  '''
  def __init__(self):
    self._procs = Processes()

  def remotepath(self):
    hjf_it_yun = 'root@100.107.70.104:/home/test_samba_share/source'

    return hjf_it_yun

  def localpath(self):
    fullpath_watch = ''
    return  fullpath_watch

  def exclude(self):
    return  [
    '^/home/source/new_branch/product/src/.vs.*',
  ]

  def sync(self, target):
    '''
    :param target: is fullpath name

    rsync /home/src 拷贝 src 目录及子目录
    rsync /home/src/ 只拷贝 src 目录下的文件

    -R 表示级联  http://ask.apelearn.com/question/1047

    http://einverne.github.io/post/2017/07/rsync-introduction.html

    同步一次 rsync -avR /home/ root@100.107.70.104:/home/

    '''

    # -R 选项之后 不再需要这个
    #remotpath = target.lstrip(self.localpath())
    #remotpath = os.path.join(self.remotepath(),remotpath)
    # 有时候不触发
    #args= ['rsync','-avR',target, self.remotepath(), '--delete']
    args= ['rsync','-avR',self.localpath(), self.remotepath(), '--delete']

    self._procs.push(args)
    self._procs.aging()

def entry(watch_directory, exclude):

  mask = IN_DELETE | IN_CREATE | IN_MODIFY | IN_CLOSE_WRITE

  handler = EventHandler()
  wm = pyinotify.WatchManager()
  notifier = AsyncNotifier(wm, handler)
  filter = ExcludeFilter(exclude)

  wdd = wm.add_watch(watch_directory, mask,
                     rec=True,  # 递归
                     auto_add=True, # 添加了新文件 新文件也会被监视 写删除那些事件
                     exclude_filter=filter
                     )

  #notifier.loop()
  asyncore.loop()


def entry2():
  entry(watch_directory=Sync().localpath(),
        exclude=Sync().exclude()
        )


if __name__ == '__main__':
    entry2()
