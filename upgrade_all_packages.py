#coding=utf-8



import pip
import subprocess

def entry():

    for dist in pip.get_installed_distributions():
        subprocess.call(['pip','install',
                         #'--proxy=',
                         '--upgrade',dist.project_name])


if __name__ == '__main__':
    entry()