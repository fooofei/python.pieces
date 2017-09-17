# coding=utf-8
'''
the file shows requests's use

记录我犯过的错误

http requests post 的使用


post 几种 Content-Type 与之对应 requests 使用方式
    application/x-www-form-urlencoded    post( data= )

    multipart/form-data; post( files=)


sessionid=...  (32 bit)
PHPSESSID=... (26 bit)
区别是什么？


'''

import requests


def upload():
  url = 'http://base'  # some url

  # 随机的参数
  param = {'arg0': '0',
           'arg1': '1', }

  # 比如上传文件
  fullpath_upload = '/home/a/a'

  with open(fullpath_upload, 'rb') as f:
    fs = {'file': f}
    req = requests.post(url, data=param, files=fs)
    assert (req.status_code == 200)

    # 这里的 post 使用 data=param 参数把键值对的参数发送出去，这是放到 http post 中的 body(消息主体)中
    # 如果使用 params=param 这是把键值对放到 url 中拼接组合起来，跟上面的不一样
    # 要能准确区分服务器接收哪种发送请求，区分上面两种使用方法


def entry():
  upload()


if __name__ == '__main__':
  entry()
