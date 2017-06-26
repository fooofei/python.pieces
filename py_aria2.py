#coding=utf-8


import os
import sys

curpath = os.path.dirname(os.path.relpath(__file__))

def is_command_exists_in_env(command):
    '''
    
    :param command: 
    :return:  True / False
    '''
    import subprocess

    try:
        with open(os.devnull,'wb') as devnull:
            p = subprocess.Popen([command, u'--version'], stdout=devnull, stderr=devnull)
            p.wait()
        return True
    except OSError:
        return False


class PyAria2(object):
    def __init__(self):
        self._path_aria2c = self._get_aria2c()

    def _get_aria2c(self):
        ''' 优先使用系统环境已有的，如果没有再使用本目录自带的 '''
        name = u'aria2c'
        if sys.platform.startswith(u'linux'):
            return name

        elif sys.platform == u'win32':
            if is_command_exists_in_env(name):
                return name
            else:
                # put executable to the path
                return os.path.join(curpath, u'bin', u'win32', name)
        else:
            return name

    def down_from_inputfile(self, path_inputfile, proxy=None):
        import subprocess

        aria2c_args=[
            self._path_aria2c,
            u'-i {0}'.format(path_inputfile),
            u'--follow-torrent=false',
            u'--auto-file-renaming=false',
            u'--allow-overwrite=false',
            u'--check-certificate=false',
            u'--connect-timeout={0}'.format(3),  # default = 60
            u'--timeout={0}'.format(5), # default = 60
            u'--max-concurrent-downloads=100',
            u'--max-tries={0}'.format(3), # default = 5
        ]

        if proxy:
            aria2c_args.append(u'--all-proxy={0}'.format(proxy))

        with open(os.devnull) as devnull:
            p = subprocess.Popen(aria2c_args, shell=False,
                                 stdout=devnull)
            try:
                p.wait()
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(e)
                # 别在这里删除这个文件
                # Windows Error 32 另一个程序正在使用此文件，进程无法访问。
                # if os.path.exists(path_inputfile):
                #    os.remove(path_inputfile)


    def write_uri_to_file(self, uris):
        '''
        :param uris: [(url,path),...]
        :return:
        '''
        import tempfile
        fd, temp_file = tempfile.mkstemp(prefix=u'aria2c_')
        with open(temp_file, 'w') as f:
            for uri, fullpath in uris:
                if not (uri and fullpath): continue
                f.write(u'{}\n'.format(uri).encode(u'utf-8'))
                d = os.path.dirname(fullpath)
                n = os.path.basename(fullpath)
                if not os.path.exists(d):
                    os.makedirs(d)
                f.write(u' dir={}\n'.format(d).encode(u'gbk'))
                f.write(u' out={}\n'.format(n).encode(u'gbk'))
        os.close(fd)
        return temp_file



def unit_test_command_exists():
    command = u'aria2c'

    print (is_command_exists_in_env(command))


def entry():
    unit_test_command_exists()



if __name__ == '__main__':
    entry()