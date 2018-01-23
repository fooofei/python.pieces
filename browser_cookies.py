#coding=utf-8

'''
the file shows how to get cookies from Chrome browser installed machine.
'''

import os


def _get_chrome_cookies_files():
  '''
  the cookies paths recorded in module browsercookie is older.
  newer Chrome's cookies is this.
  '''
  import glob
  p1 = os.getenv('APPDATA', '')
  fullpath_chrome_cookies = os.path.join(p1,r'..\Local\Google\Chrome\User Data\Profile 1\Cookies')
  for e in glob.glob(fullpath_chrome_cookies):
    yield e


def _get_chrome_cookies():
  '''
  return type is RequestsCookieJar
  on macOS, may need use authority check
  '''
  import browsercookie
  from itertools import chain

  a = browsercookie.Chrome()
  files_old = a.find_cookie_files()
  files = chain(_get_chrome_cookies_files(), files_old)
  return browsercookie.chrome(files)
