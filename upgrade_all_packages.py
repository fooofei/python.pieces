# coding=utf-8

'''
the file shows how to upgrade all packages use in local python
'''

import pip
import subprocess
import sys


def entry():
  c = []
  if sys.platform.startswith('linux'):
    c.append('sudo')
  c.extend(['pip', 'install',
            # '--proxy=',
            '--upgrade'])
  for dist in pip.get_installed_distributions():
    subprocess.call(c + [dist.project_name])


if __name__ == '__main__':
  entry()
