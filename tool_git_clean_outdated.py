# coding=utf-8
'''
有些本地分支在远端已经不存在了，提供脚本删除
'''

import git
import os
import sys
from pathlib import Path

curpath = Path(__file__).absolute().parent


def clean_outdated(local_repo):
    g = git.Repo(local_repo)
    branches = g.branches
    branches = list(branches)
    if len(branches) < 1:
        print(f"[!] Not found any valid local branch")
        return
    remotes = g.remotes
    remotes = list(remotes)
    if len(remotes) < 1:
        print(f"[!] Not found any valid remotes")
        return
    remote = remotes[0]
    print(f"{remote.url} {g.active_branch}")
    print(f"Fetching ...")
    r = remote.fetch()
    for value in list(r):
        print(f"  {value}")

    valid_branches = []
    invalid_branches = []
    # `git branch -vv | grep ': gone]' | awk '{print $1}'`
    for branch in branches:
        trk_branch = branch.tracking_branch()
        if trk_branch is not None and trk_branch.is_valid():
            valid_branches.append(branch)
        else:
            invalid_branches.append(branch)

    print("")
    print(f"Stay branches:")
    if len(valid_branches) < 1:
        print(f"  No valid branch")
    for b in valid_branches:
        print(f"  {b}")
    print("")
    print(f"Not exists in remote branches:")
    if len(invalid_branches) < 1:
        print(f"  No invalid branch")
    for b in invalid_branches:
        print(f"  {b}")

    if len(invalid_branches) > 0:
        ch = input("Delete all `[-]` ? Y or y for yes:")
        if ch not in ["Y", "y"]:
            return
        print(f"Deleting ...")
        # git branch -D
        g.delete_head(*invalid_branches, force=True)  # no return value


if __name__ == '__main__':
    try:
        clean_outdated(curpath)
    except Exception as er:
        print(f"{type(er)} {er}")
    os.system("pause")
