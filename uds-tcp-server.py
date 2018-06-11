#coding=utf-8
'''

Windows has recently (Windows 10 Insider build 17063) implemented support for AF_UNIX,
 so you can use it in future windows builds.
'''

import os
import sys
import socket
import uuid
import time


curpath = os.path.dirname(os.path.realpath(__file__))

def entry():
    name = uuid.uuid1()
    #name = .format(u=name)
    name = 'uds_socket_demo'
    addr = os.path.join(curpath,os.path.join(curpath,name))

    if os.path.exists(addr):
        os.unlink(addr)

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)

    sock.listen(1)

    print('listening')

    conn,sdaddr = sock.accept()
    print('got sendaddr {ad}'.format(ad=sdaddr))
    i=0
    while i<1000:
        content = "hello"*110
        content = '{0}{1}\n'.format(i,content)
        conn.send(content)
        time.sleep(0)
        i+=1

    conn.send('end')
    conn.close()
    os.remove(addr)
    print('Alread sent {c} msgs'.format(c=i))


if __name__ == '__main__':
    entry()
