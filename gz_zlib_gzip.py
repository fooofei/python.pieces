#coding=utf-8

'''
这个文件用来测试当 HTTP 请求头部中携带了
Content-Encoding: gzip\r\n
无论是 Request 还是 Response 吧，咱不区分

如果携带了，应该用什么库函数解压压缩呢？

Python 中是 gzip 模块不是 zlib 模块。

'''

import os
import sys

import zlib
import gzip
import binascii
from io import BytesIO
from io import StringIO


test_content_gzip_bin= '''1f8b08000000000004008494c94aa34114854b5ae865bbea6db2ecc7e8c7e9c768445134e6ff09d11887c409c504a3821a158206278c4829e28012094ec161115c080ef075ddbf680b9b6057b8dc3a37f79c7baa4845a906f3696a921c56bf1a95faae94fa61c2944cc5d665fd6c0cd2a78bf6f69009cf84a6ad8d205a5b352d2d1ecdcda14fb9d1a887e7f11ed12874754124021d1d184dd1f2ea72e3714d7737f4f4b8101c8f432c06be6ff53a3b45477fe026931efdfd30300083832e044b3d998444c269599dc007a95488a121181981d151181b732158eaf27d2a65b57a7bad8ef8894442a62fcdc4044c4e422603ababbc2fc1523f38b0f8f9d9eaf6f5d9f3c56269b259cdd4144c4fc3ec2c6c6c38beece7e6e0e5c5e2ed6dcb173f72b64442071ce9595880c545d8d971fcd757b8bab2fba727c8e5aca7f171181eb61af93c2c2f43a1002b2bb0b747dd25b3658ef8cc669d46a1a02916617d1d3637e1f0d071dede9c0fe9595a82f9799899f9aba1595b4bb3b505a512eceec2e9a9e31f1db9fdc383f5275e45437c643269e32b1cf0f6f7ed3d572a8e23f8e2c2e1db5bab213ee42cb95cf0304c9fc7f1b19d7d7e0e3737707d6db1d4cfcedc5ebcca5de5f31f7ec794cb3a987d7969ef5cb2e072194e4eac17f129fc6251d77d03d5aacfdd1ddcdf13e46ad5fa170d992d672c95fc4fdf60ad16e6f1d137590777261a958a36fe7de321fc6f7fed9b5295af4aad7e51ea77c3ffff1fa4477a8523dc3f03001ec652737e040000
'''

def test_zlib(fp):
    with open(fp, "rb") as fr:
        hex_stream = fr.read()
        hex_stream = hex_stream.strip()
        print("len(hex stream)= {}".format(len(hex_stream)))
        hexv = binascii.unhexlify(hex_stream)
        a = zlib.decompress(hexv)
        print(a)

def test_gzip(fp):
    with open(fp, "rb") as fr:
        hex_stream = fr.read()
        hex_stream = hex_stream.strip()
        print("len(hex stream)= {}".format(len(hex_stream)))
        hexv = binascii.unhexlify(hex_stream)
        with gzip.GzipFile(fileobj=BytesIO(hexv)) as frz:
            a = frz.read()
            print(a)
def main():
    p = "/Downloads/Untitled-1"
    test_zlib(p)
    pass

if __name__ == '__main__':
    main()
