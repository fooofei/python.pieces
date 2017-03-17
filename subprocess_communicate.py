# coding=utf-8
from __future__ import unicode_literals


def amr2avi():
    '''
    amr 批量转换为 avi
    此函数可以学习
        1. 如何向子进程发送数据 subprocess.communicate

        2. subprocess.Popen, shell 参数:
            shell = False (default) , 执行参数应该是 list, 封装为 [<待执行二进制>, <arg0>,<arg1>,...]
            shell = True, 执行参数可以是 str, 可以传递 '{} {} {}'.format(<待执行二进制>, <arg0>,<arg1>)

    :return:
    '''
    import subprocess
    pathf = r''
    runexe = r''
    for e in os.listdir(pathf):
        if e.endswith('.amr'):
            cmd = '{0} {1}'.format(runexe, os.path.join(pathf, e))
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
            p.communicate(input='\n') # 这里需要向子进程中填入 \n 来继续运行，是因为子程序是这样写的


if __name__ == '__main__':
    amr2avi()
