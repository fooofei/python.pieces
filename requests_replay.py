#coding=utf-8

'''
在拥有一个 HTTP 抓包的情况下，如何快速直接回放 HTTP 请求

抓包 HTTP 格式为
POST /v2/reward_tasks/4/rewards HTTP/1.1
Host: lucky.nocode.com
version: 0.10.12
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMzEyNTMyLCJpYXQiOjE1NjAyNDcxNjksImV4cCI6MTU2MDg1MTk2OX0.8HD0iCFPZywo1qB6IBD2xlySb2SOdQEWobD9p6s4FZ4
timestamp: 1560301564990
Accept: */*
Client-Version: 7.0.4
Accept-Language: zh-cn
Accept-Encoding: br, gzip, deflate
platform: wechat
X-Request-ID: 40bdced0-8cae-11e9-be07-07d38dcffb06
Content-Length: 46
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.4(0x17000428) NetType/WIFI Language/zh_CN
Referer: https://servicewechat.com/wx01bb1ef166cd3f4e/379/page-frame.html
Connection: keep-alive
Content-Type: application/json
sign: ec42ec6b2d3be4fe27c551d01cd5e4ea3846619d

{"form_id":"5dd95790b967445f8f83966655d7a41c"}

CRLF 换行分割
'''

import os
import sys
import requests
from timeit import default_timer as Time
import hashlib
from json import loads as json_loads
from json import dumps as json_dumps
from requests_toolbelt.utils import dump as resp_dump
from http_parser.pyparser import HttpParser
from time import sleep


def tx_req_from_raw_request(filename):
    '''
    把 plaintext 的请求 解析后，做重放
    '''
    headers_raw = ""
    with open(os.path.join(filename), "rb") as fr:
        headers_raw = fr.read()

    hp = HttpParser()
    r = hp.execute(headers_raw, len(headers_raw))
    print("{} len={} parsed={}".format(filename, len(headers_raw), r))
    headers = dict(hp.get_headers())
    body = hp.recv_body()
    url = f'''https://{headers.get("HOST", "")}{hp.get_path()}'''
    method = hp.get_method().lower()
    resp = requests.request(method=method, url=url, headers=headers, data=body)
    print(resp_dump.dump_all(resp))
    print("\n\n")
