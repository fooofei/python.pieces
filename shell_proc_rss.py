# coding=utf-8

'''
每 3s 打印占用内存

'''

import os
import sys
from time import sleep
import sh
from datetime import datetime


def get_process_pid(pname):
    cmd_ps = sh.Command("/bin/ps")
    cmd_grep = sh.Command("/bin/grep")
    cmd_awk = sh.Command("/bin/awk")
    # _iter=True
    # use _ok_code to ignore exception 
    all_process = cmd_ps("-efww", _piped=True, _ok_code=[0, 1, 2, 3])
    all_sfu1 = cmd_grep(all_process, pname, _piped=True, _ok_code=[0, 1, 2, 3])
    all_sfu2 = cmd_grep(all_sfu1, "-v", "sshd", _piped=True, _ok_code=[0, 1, 2, 3])
    all_sfu3 = cmd_grep(all_sfu2, "-v", "grep", _piped=True, _ok_code=[0, 1, 2, 3])
    all_sfu4 = cmd_grep(all_sfu3, "-v", "gdb", _piped=True, _ok_code=[0, 1, 2, 3])
    fiterd_sfu = cmd_awk(all_sfu4, "{print $2}", _ok_code=[0, 1, 2, 3])
    stdout = fiterd_sfu.stdout
    stdout = stdout.strip()
    stdout = stdout.rstrip("\r\n")
    return stdout


def main():
    '''
    如何得到 vmrss 数字字段
    # (Pdb) p vmrss.split(' ')  ['VmRSS:\t', '', '', '', '3976', 'kB']
    vmrss = (vmrss.split(' ')[-2])
    vmrss = vmrss.split('\t')[-1]
    vmrss = int(vmrss)
    '''
    arg_pid = ""
    if len(sys.argv) > 1:
        arg_pid = sys.argv[1]
    while True:
        pid = arg_pid
        if pid == "":
            pid = get_process_pid("test")
        if pid == "" or "\n" in pid:
            print("{} got invalid pid `{}`".format(datetime.now(), pid))
        else:
            proc_path = "/proc/{}/status".format(pid)
            print("{} read {}".format(datetime.now(), proc_path))
            try:
                with open(proc_path, "r") as fr:
                    for l in fr:
                        if "RSS" in l:
                            print(l)
            except IOError:
                pass
        sleep(1)


if __name__ == '__main__':
    main()
