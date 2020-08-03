# coding=utf-8
'''
把主仓库的当前分支同步到我的 fork

pip install gitpython

ref https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/merging-an-upstream-repository-into-your-fork
'''

import git
import os
import sys
from pathlib import Path

curpath = Path(__file__).absolute().parent


def sync_my_fork(local_repo):
    g = git.Repo(local_repo)
    if len(g.remotes) < 1:
        print(f"[!] Cannot get valid remote url")
        return
    gr = g.remotes[0]
    url = gr.url
    branch = g.active_branch
    print(f"url=`{url}` branch=`{branch}`")
    url = url.replace("<fork>", "<remote main repo>")
    print(f"sync from")
    print(f"  {url}")
    print(f"  {branch}")
    print(f"command git pull {url} {branch}")
    r = gr.repo.git.pull(url, branch)
    print(r)


if __name__ == '__main__':
    try:
        sync_my_fork(curpath)
    except Exception as er:
        print(f"{type(er)} {er}")
    os.system("pause")
