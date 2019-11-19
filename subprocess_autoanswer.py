# coding=utf-8
'''
这个文件演示进程启动后做到自动回答某些提示
'''

import os
import sys
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from subprocess import call

from fabric import Connection
from invoke import Responder


def main_subprocess():
    '''
    通过 subprocess 模块实现自动回答  失败
    '''
    # 自定义启动命令
    args = []
    home = os.path.dirname(args[2])
    # 只要有了 stdin=PIPE 就没提示输入了 很奇怪
    # 这里说不需要等
    # https://stackoverflow.com/questions/54319960/wait-for-a-prompt-from-a-subprocess-before-sending-stdin-input
    p = Popen(args=args, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=home)

    answer = "1231232\r\n".encode("utf-8")

    # ret = p.communicate(input=)
    p.stdin.write(answer)
    p.stdin.flush()
    p.stdin.close()
    ret = p.wait()
    print("ret= {}".format(ret))
    print("out={}".format(p.stdout.read()))
    print("err={}".format(p.stderr.read()))


def main():
    '''
    使用 fabric 做自动回答 成功了
    '''
    # 自定义启动命令
    args = []
    home = os.path.dirname(args[2])
    os.chdir(home)
    answer = Responder(
        pattern="Please enter the password",
        response="2232\n"
    )
    with Connection("127.0.0.1") as c:
        cmd = {"command": " ".join(args), "hide": True, "warn": True,
               "encoding": "utf-8", "pty": True, "watchers": [answer]}
        ret = c.local(**cmd)
        # print("ret={} {}".format(type(ret), ret))


if __name__ == '__main__':
    main_subprocess()
