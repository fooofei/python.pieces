#coding=utf-8

'''
这个文件用来聚合 在 python 中与 shell 有关联的操作

还有一个独立的文件 subprocess_idioms.py 来记录
subprocess 模块使用的技法

在 python 中，最推荐的 shell 模块，做自动化时，
应该是 sh 第三方模块了。
https://amoffat.github.io/sh/

_cwd=curpath, 
_out=sys.stdout, 
_err=sys.stdout
_ok_code=[0, 1] # 用来避免抛异常

'''

import sh

def change_shell_env():
    '''
        The file shows how to change the login shell environment
        没找到办法

        20190620 更新，忘记我为什么说没找到方案了，
        现在来看，如果是 subprocess 启动的进程，是可以做到动态设置 env 的

        '''

    # ref https://stackoverflow.com/questions/38982640/set-shell-environment-variable-via-python-script
    # ref https://stackoverflow.com/questions/35780715/setting-environment-variables-of-parent-shell-in-python
    # ref https://stackoverflow.com/questions/8365394/set-environment-variable-in-python-script
    pass




def sh_asterisk():
    '''
    如果遇到要传递参数为 * 的命令，应该怎么做
    https://stackoverflow.com/questions/32923189/how-to-pass-an-asterisk-to-module-sh-in-python
    '''
    # 等价 linux 命令 tar czf 1.tar.gz *
    sh.tar("czf", "1.tar.gz", sh.glob("*"))

