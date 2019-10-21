# coding = utf-8

'''
记录研究结果 
```
paramiko.Transport.set_keepalive(interval)
```
会每隔 interval 发送 1 次 TCP keepalive，payload =0
在业务应用中，还是不合适的。

'''

import os
import sys
import paramiko


if __name__ == "__main__":
    pass
