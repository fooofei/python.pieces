#coding=utf-8


import os
import sys
from fabric import Connection as SSHConnection


def main():

    hosts=[
    ]

    upgrade_commands =[

    ]

    commands=[
        'lscpu'
    ]


    for host in hosts:
        cnn = SSHConnection(host=host[0], user=host[1],
                            port=22, connect_kwargs={'password': host[2]})
        for command in commands:
            # hide is not show the result auto
            rc = cnn.run(command, hide=True)
            print('{} {} return_code={} stderr={} stdout={}'.format(
                rc.connection.host,
                rc.command, rc.return_code, rc.stderr, rc.stdout))
            print('\n\n')
        cnn.close()

if __name__ == '__main__':
    main()
