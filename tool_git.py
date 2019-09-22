#coding=utf-8
'''
通过 python 读取 某个 git repo 的 commit log
以单元读取 然后针对单元做过滤 做统计

https://github.com/gitpython-developers/GitPython

'''

import git
import os
import sys

curpath = os.path.dirname(os.path.realpath(__file__))

def read_alllog():
    '''
    A sample:
    commit bbfc446613462580f8b935bde8bf1b5e74bd4ec5
    Author: fooofei <aihujianfei@qq.com>
    Date:   Wed Apr 26 11:48:51 2017 +0800

        + write gzip

    commit 8e4cd3470418e7828d2ada3fdfe1cddf345afb1d
    Author: fooofei <aihujianfei@qq.com>
    Date:   Tue Apr 18 20:19:55 2017 +0800

        1

    commit 991182ceed469966006edd8303f38e5d2c942c37
    Author: fooofei <aihujianfei@qq.com>
    Date:   Tue Apr 18 20:18:23 2017 +0800

    + yield
    :return:
    '''
    path_git_repo = curpath

    g = git.Git(path_git_repo)
    result = g.log()
    print(result)

def dict_addint(dest, src):
    for k,v in src.iteritems():
        dest.setdefault(k,0)
        dest[k] += v

def read_unitcommits():
    path_git_repo = curpath

    rpo = git.Repo(path_git_repo)
    cmt_total= {'deletions': 0, 'lines': 0, 'insertions': 0}
    cmt_count = 0

    for cmt in rpo.iter_commits():
        # cmt.author.email
        # cmt.author.name
        # cmt.committer.email
        # cmt.committer.name
        # 按照 邮件地址过滤

        for k,v in cmt.stats.files.iteritems():
            if k.find('io_in_out') != -1:
                print(u'{0}'.format(k))
                print(u'    {0}'.format(v))
                cmt_count += 1
                dict_addint(cmt_total,v)

        # 查看源码 发现对比的是本次提交与 parent[0] ，self.repo.git.diff(self.parents[0].hexsha, self.hexsha, '--', numstat=True)
            #   我发现有时候存在多个 parent，那么会不会丢失其他 parent 呢
            #  不会 不丢失 我对比过 log
            #io_in_out.io_print(u'  {}'.format(cmt.stats.total))

    print(u'总计 提交次数 {0} {1}'.format(cmt_count, cmt_total))

if __name__ == '__main__':
    #read_alllog()
    read_unitcommits()
