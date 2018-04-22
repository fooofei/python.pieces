# -*- coding=UTF-8 -*-


'''
输入输出函数

其他脚本中的进入的字符串参数和输出到屏幕的字符串参数都需要经过转换
进入的字符串需要转为 unicode （为了支持路径中的中文）
输出到屏幕的字符串需要从 unicode 转为 str （为了兼容重定向符号 > ,某些时候我们需要把脚本运行结果重定向到文件）

兼容 python 2.6, 2.7, 3

scandir.walk  benchmark :

    # 7w files
    for e in io_iter_files_from_arg(sys.argv[1::]) :
        pass
    os.walk - 1.16999983788
    scandir.walk - 0.280000209808

'''

# ------------------------------------------------------------------------------
# feedback : fooofei
# CHANGELOG:
# 2017-02-22 v2.00 修复其他国语言编码异常
# 2017-02-23 v2.10 add io map
# 2017-03-14 v2.20 io_out_arg 增加参数
# 2017-04-28 v2.30 add io_iter_split_step(), 一步步取文件，在遇到大量文件的时候，可以指定步长取文件，比如 10000 一次
# 2017-05-02 v2.30 add io_path_format()
# 2017-05-16 v2.40 add io_is_process_run_in_visual_studio()
# 2017-05-16 v2.50 add io_iter_split_step_pre()
# 2017-05-30 v2.60 add __all__
# 2017-06-21 v2.70 add io_render_to_html()
# 2017-07-31 v2.80 os.walk() 可能返回非 unicode 编码字符串，会导致异常
# 2017-07-31 v2.90 add io_multiprocessing_thread_map_one_ins() 兼容 python2.6
# 2017-08-01 v2.91 add 梳理 io path encoding


from __future__ import with_statement
from __future__ import print_function
import os
import sys

try:
    from scandir import walk as local_walk
except ImportError:
    from os import walk as local_walk

__all__ = [
]

pyver = sys.version_info[0]  # major
sys_platform = sys.platform
if pyver >= 3:
    io_binary_type = bytes
    io_text_type = str
    io_raw_input = input
    io_integer_types = (int)
else:
    io_raw_input = raw_input
    io_binary_type = str
    io_text_type = unicode
    io_integer_types = (int, long)
io_str_codecs = (io_text_type, io_binary_type)
io_terminal_encoding = 'utf-8'
if sys.stdout.isatty(): io_terminal_encoding = sys.stdout.encoding
io_filesystem_encoding = sys.getfilesystemencoding()  # operating system depending encoding


def io_text_arg(arg, encoding=None, pfn_check=None):
    '''
    :param encoding: tuple (,)
    :param pfn_check: to check the convertion is right
    '''

    if not arg: return arg
    if isinstance(arg, io_text_type): return arg
    if not pfn_check: pfn_check = lambda x: x
    encodings = []
    if encoding and isinstance(encoding, (tuple, list)):
        encodings.extend(list(encoding))
        encodings = filter(lambda x: x, encodings)
        encodings = list(encodings)
    encodings.extend(['utf-8', 'gb18030', 'gbk', 'windows-1250'])
    er = None
    for c in encodings:
        try:
            v = arg.decode(c)
            if pfn_check(v): return v
        except UnicodeDecodeError as er0:
            er = er0
    raise (er or ValueError('decoding error {0} maybe not exists'.format(arg)))


def io_bytes_arg(arg, encoding=None, pfn_check=None):
    '''python 与 ctypes 交互也用这个， ctypes 需要 py3 中的 bytes 类型
    '''

    if not arg: return arg
    if not isinstance(arg, io_text_type): return arg
    if not pfn_check: pfn_check = lambda x: x
    encodings = []
    if encoding and isinstance(encoding, (tuple, list)):
        encodings.extend(list(encoding))
        encodings = filter(lambda x: x, encodings)
        encodings = list(encodings)
    encodings.extend(['utf-8', 'gb18030', 'gbk'])

    er = None
    for c in encodings:
        try:
            v = arg.encode(c)
            if pfn_check(v): return v
        except UnicodeEncodeError as er0:
            er = er0
    raise (er or ValueError(u'encoding error {0} maybe not exists'.format(arg)))


def io_text_filesystem_path(arg):
    try:
        return io_text_arg(arg,
                           encoding=(io_filesystem_encoding,),
                           pfn_check=os.path.exists)
    except UnicodeDecodeError:
        return None


def io_bytes_filesystem_path(arg):
    try:
        return io_bytes_arg(arg,
                            encoding=(io_filesystem_encoding,),
                            pfn_check=os.path.exists
                            )
    except UnicodeEncodeError:
        return None


def io_iter_files_from_arg(args):
    ''' No UnicodeEncodeError()
    问题：bytes 编码的路径 能 walk，之后 decode 之后变成 unicode ，os.path.exists 失效了'''
    for e in args:
        if os.path.isfile(e):
            v = io_text_filesystem_path(e)
            if v: yield v
        elif os.path.isdir(e):
            # 有些路径不可以被转换到 unicode
            e = io_bytes_filesystem_path(e)
            for root, sub, files in local_walk(e):
                for i in files:
                    v = os.path.join(root, i)
                    v = io_text_filesystem_path(v)
                    if v: yield v
    raise StopIteration


def io_iter_root_files_from_arg(args):
    for e in args:
        if os.path.isfile(e):
            v = io_text_filesystem_path(e)
            if v: yield v
        elif os.path.isdir(e):
            e = io_bytes_filesystem_path(e)
            for sub in os.listdir(e):
                p = os.path.join(e, sub)
                if os.path.isfile(p):
                    v = io_text_filesystem_path(p)
                    if v: yield v
    raise StopIteration


def _io_standard_write(writer, arg):
    # Terminal use Terminal's encoding, else use utf-8
    encoding = io_terminal_encoding
    arg = io_bytes_arg(arg, encoding=(encoding,))
    # py3 use sys.stdout.buffer.write
    # py2 use sys.stdout.write
    return getattr(writer, 'buffer', writer).write(arg)


def io_sys_stdout(arg):
    return _io_standard_write(sys.stdout, arg)


def io_sys_stderr(arg):
    return _io_standard_write(sys.stderr, arg)


def io_print(arg):
    arg = u'{0}'.format(arg)
    io_sys_stdout(arg)
    print('', file=sys.stdout)
    sys.stdout.flush()


def io_stderr_print(arg):
    arg = u'{0}'.format(arg)
    io_sys_stderr(arg)
    print('', file=sys.stderr)
    sys.stderr.flush()


def io_files_from_arg(args):
    return list(io_iter_files_from_arg(args))


def io_is_path_valid(pathname):
    '''
    路径是否有效
    http://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
    :param pathname:
    :return: bool
    '''
    import errno
    ERROR_INVALID_NAME = 123
    try:
        _, pathname = os.path.splitdrive(pathname)
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') if sys.platform == 'win32' else os.path.sep
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in [errno.ENAMETOOLONG, errno.ERANGE]:
                    return False
    except TypeError:
        return False
    else:
        return True


def io_path_format(fullpath, replace_with=None):
    '''
    remove forbidden chars in path
    :param fullpath: 
    :return: 
    '''
    if not isinstance(fullpath, io_text_type):
        raise ValueError(u'only support type {0}'.format(io_text_type))

    windows_path_forbidden_chars = u'\\/*?:"<>|'
    remove_map = dict((ord(char), replace_with if replace_with else None) for char in windows_path_forbidden_chars)
    return fullpath.translate(remove_map)


def io_thread_map(thread_func, thread_data, max_workers=20):
    '''
    等价于 :
        for e in thread_data:
            r = thread_func(e)

    返回的结果顺序与参数 thread_data 提供的顺序一致

    即便是保持了顺序 但是也不是说没并行 还是存在并行的

    '''

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        r = pool.map(thread_func, thread_data)
        pool.shutdown(wait=True)
        return list(r)


def io_multiprocessing_thread_map_one_ins(thread_func, thread_data, ins_generator_func, max_workers=8):
    '''
    等价于 :
        for e in thread_data:
            r = thread_func(ins_generator_func(),e)
    区别于 io_thread_pool : 适用于 1 个线程 1 个实例的情景
    '''
    import threading
    from multiprocessing.pool import ThreadPool

    thread_local_data = threading.local()

    def _func_in_thread(every_thread_data):
        try:
            thread_local_data.ins
        except AttributeError:
            thread_local_data.ins = ins_generator_func()
        return thread_func(thread_local_data.ins, every_thread_data)

    a = ThreadPool(processes=max_workers)
    r = a.map(_func_in_thread, thread_data)
    return r


def io_thread_map_one_ins(thread_func, thread_data, ins_generator_func, max_workers=8):
    '''
    等价于 :
        for e in thread_data:
            r = thread_func(ins_generator_func(),e)
    区别于 io_thread_pool : 适用于 1 个线程 1 个实例的情景
    '''
    import threading
    from concurrent.futures import ThreadPoolExecutor

    thread_local_data = threading.local()

    def _func_in_thread(every_thread_data):
        try:
            thread_local_data.ins
        except AttributeError:
            thread_local_data.ins = ins_generator_func()
        return thread_func(thread_local_data.ins, every_thread_data)

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        r = pool.map(_func_in_thread, thread_data)
        pool.shutdown(wait=True)
        return list(r)


def dict_item_getter(data, keys):
    '''
      dict_item_getter({'1': {'2': {'3': 'hello'}}}, ['1', '2', '3']) = 'hello'
    '''
    f = lambda x, y: x[y] if y in x else None
    return reduce(f, keys, data)


def io_directory_merge(src, dst):
    '''

    需求 ： 把 sub 目录整体移动到 parent 内，效果为： parent/sub
         如果 parent 目录内已经有 sub 目录，则覆盖合并，已存在的同名文件覆盖


    def unit_test_shutil_copytree():

        不符合需求，此调用要求 parent 目录必须不存在

        import shutil
        parent = r"F:\everysamples\0000\bbs\2\parent"
        sub = r"F:\everysamples\0000\bbs\2\sub"
        shutil.copytree(sub,parent)

    def unit_test_distutils_dir_util():
        from distutils.dir_util import copy_tree,remove_tree
        parent = r"F:\everysamples\0000\bbs\2\parent"
        sub = r"F:\everysamples\0000\bbs\2\sub"

        if not (not os.path.exists(parent) or os.path.isdir(parent)):
            raise ValueError('parent must not exist or is dir')
        copy_tree(src=sub,dst=os.path.join(parent,os.path.basename(sub)))
        remove_tree(directory=sub)
        '''
    from distutils.dir_util import copy_tree, remove_tree

    if not (not os.path.exists(dst) or os.path.isdir(dst)):
        raise ValueError('parent must not exist or is dir')
    # src must be an exist directory
    # 如果文件存在会自动覆盖
    copy_tree(src=src, dst=os.path.join(dst, os.path.basename(src)))
    remove_tree(directory=src)


def shutil_force_copy(src, dest):
    '''EAFP way, avoid races and unneeded syscalls'''
    try:
        shutil.copy(src, dest)
    except IOError as er:
        if er.errno != errno.ENOENT:
            raise
        os.makedirs(os.path.dirname(dest))
        shutil.copy(src, dest)


def io_hash_stream(stream, hash_algorithm=u'md5', block_size=2 ** 20):
    import hashlib
    hash_ins = {u'md5': hashlib.md5(),
                u'sha1': hashlib.sha1()}.get(hash_algorithm, None)
    if not hash_ins:
        raise ValueError('not get proper hash algorithm')
    while 1:
        data = stream.read(block_size)
        if not data:
            break
        hash_ins.update(data)
    return hash_ins.hexdigest()


def io_hash_memory(memory, hash_algorithm=u'md5'):
    from io import BytesIO
    with BytesIO(memory) as f:
        return io_hash_stream(f, hash_algorithm)


def io_hash_fullpath(fullpath, hash_algorithm=u'md5'):
    with open(fullpath, 'rb') as f:
        return io_hash_stream(stream=f, hash_algorithm=hash_algorithm)


def io_line_is_hash(line):
    import re
    return (re.match(u"[a-fA-F\d]{64}", line) or
            re.match(u"[a-fA-F\d]{40}", line) or
            re.match(u"[a-fA-F\d]{32}", line))


def _io_simple_check_hash(line, hash_length):
    fn = lambda e: all(i in '1234567890abcdefABCDEF' for i in e)
    return len(line) == hash_length and fn(line)


def io_simple_check_md5(line):
    return _io_simple_check_hash(line, 32)


def io_simple_check_sha1(line):
    return _io_simple_check_hash(line, 40)


def io_simple_check_sha256(line):
    return _io_simple_check_hash(line, 64)


def io_simple_check_hash(line):
    return io_simple_check_md5(line) or io_simple_check_sha1(line) or io_simple_check_sha256(line)


def _io_iter_split_step(data, split_unit_count):
    '''
    :param data:  must be isinstance(data, collections.Iterable):
    :param split_unit_count: 
    :return: generator object  iter(tuple)

    see test
    '''
    a = iter(data)
    while True:
        r = []
        for _ in range(0, split_unit_count):
            try:
                e = next(a)
                r.append(e)
            except StopIteration:
                if r:
                    yield tuple(r)
                    r = []
                else:
                    raise StopIteration
        if r:
            yield tuple(r)
            r = []


def io_iter_split_step(data, split_unit_count):
    '''
    :param data:  must be isinstance(data, collections.Iterable):
    :param split_unit_count: 
    :return: generator object  iter(tuple)

    see test
    '''

    from itertools import islice
    i = iter(data)
    while True:
        # slice return iterable
        r = tuple(islice(i, split_unit_count))
        if not r: break
        yield (r)


def io_iter_split_step_pre(data, split_unit_count):
    '''
    return 300 items at first, for test small data
    '''
    import itertools
    tasksi = iter(data)
    pre = itertools.islice(tasksi, 300)
    pre = tuple(pre)
    if pre: yield pre
    for i in io_iter_split_step(tasksi, split_unit_count):
        yield i


def io_sequence_function(initial, function_sequence):
    '''
    :param initial: 
    :param function_sequence: list of Functions
    :return: the last function result
    
    equivalent :
        def foo(initial):
            initial = function_sequence[0](initial)
            initial = function_sequence[1](initial)
            initial = function_sequence[2](initial)
            initial = function_sequence[...](initial)
            return initial
    
    Usage:
    
        def f1(x):
            print ('call f1')
            if x >1 :
                return int(x)+1
            return None
    
    
        def f2(x):
            print ('call f2')
            if x >5 :
                return x+10
            return None
        
        def f3(x):
            print ('call f3')
            if x > 10:
                return x+100
            return None
    
        
        # _fn = lambda x,y : y(x) if x else None  # 不符合条件的 x 没有使用 y 调用会导致后面的函数无法调用到
        如以下测试结果
        fs = [f1,f2,f3]
        print (io_sequence_function(0,fs)) 
        None
        
        print (io_sequence_function(1,fs))
        call f1
        None
        
        print (io_sequence_function(7,fs))
        call f1
        call f2
        call f3
        118
        
        使用 _fn = lambda x,y : y(x) 运行结果：
        fs = [f1,f2,f3]
        print (io_sequence_function(0,fs)) 
        call f1
        call f2
        call f3
        None
                
        print (io_sequence_function(1,fs))
        call f1
        call f2
        call f3
        None
                
        print (io_sequence_function(7,fs))
        call f1
        call f2
        call f3
        118
        
    '''
    _fn = lambda x, y: y(x)
    fs = [initial]
    fs.extend(function_sequence)
    return reduce(_fn, fs)


def io_is_process_run_in_visual_studio():
    import psutil
    p = psutil.Process().parent()
    return u'devenv.exe' == p.name() and u'Microsoft Visual Studio' in p.exe()


def io_from_timestamp(ts):
    '''
    timestamp int to datetime
	1496121889734 -> 2017-05-30 13:24:49.734000
    '''
    import datetime

    ts_str = str(ts)
    if not ts_str.isdigit():
        raise ValueError('timestamp must be digit')
    if len(ts_str) == 10:
        ts = int(ts)
    elif len(ts_str) == 13:
        ts = float(int(ts)) / 1000
    elif not (ts == 0):
        raise ValueError('unexcept timestamp format {0}'.format(ts_str))
    return datetime.datetime.fromtimestamp(ts)


def io_render_to_html(template_fullpath, *args, **kwargs):
    '''
    A sample :
    values = {
        u'ext_info':u'测试info',
        u'tables':[
            {
                u'name':u'第一个表',
                u'headers':[u'名字',u'年龄'],
                u'header_color':'#CCCC00',
                u'values':[
                    { u'color':'#99CC00',
                      u'values':[{u'color':'#FF6666',u'value':u'小红'},{u'color':'',u'value':u'30'},],
                    },
                    {
                        u'color':'CCCC00',
                        u'values':[{u'color':'',u'value':u'宝能'},{u'color':'#0066CC',u'value':u'23'},],
                    },


                ]
            },
        ]
    }
    '''
    import jinja2
    if template_fullpath is None:
        template_fullpath = os.path.dirname(os.path.realpath(__file__))
        template_fullpath = os.path.join(template_fullpath, u'template.html')
    loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_fullpath))
    env = jinja2.Environment(loader=loader)
    # can not use absolute path , jiaja2 bug
    template = env.get_template(os.path.basename(template_fullpath))
    return template.render(*args, **kwargs)


def io_size_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return u"%.1f%s%s" % (num, 'Yi', suffix)


def io_windows_filetime_to_datetime(win_ft):
    import datetime
    # to unix time
    epoch = divmod(win_ft - 116444736000000000, 10000000)
    if epoch[0] < 0: epoch = (0,) + epoch[1::]
    return datetime.datetime.fromtimestamp(epoch[0])


'''
end
'''


def test_unicode_print():
    '''
    python 2 windows
        print  encoding=cp936
        print > encoding=None
    python 3 windows
        print encoding=utf-8
        print > encoding=cp936

    python 2 linux
        print encoding=utf-8
        print > encoding=None

    python 3 linux
        print encoding=utf-8
        print > encoding=utf-8

    '''
    io_print(u'你好中国')


def test_path():
    ''' create dir u'中国/中国' for test'''
    import os
    import functools
    io_stderr_print(u'isatty:{0}'.format(sys.stdout.isatty()))
    io_stderr_print(u'stdout_encoding:{0}'.format(sys.stdout.encoding))

    f = functools.partial(io_text_arg, encoding=(sys.stdout.encoding,))
    fs = map(f, sys.argv[1::])
    p = io_iter_files_from_arg(fs)
    for e in p:
        io_sys_stdout(u'type:{0} {1}'.format(type(e), e))
        io_print(u' path_valid:{0}'.format(io_is_path_valid(e)))


def test_io_is_path_valid():
    '''
    c:\1->valid
    c:\21?->invalid
    c:\21*->invalid
    c:\21:->invalid
    c:\21"->invalid
    c:\21|->invalid
    c:\21<->invalid
    c:\21>->invalid 
    '''

    _func = lambda p: u'{}->{}'.format(p, u'valid' if io_is_path_valid(p) else u'invalid')

    io_print(_func(u'c:\\1'))
    io_print(_func(u'c:\\21?'))
    io_print(_func(u'c:\\21*'))
    io_print(_func(u'c:\\21:'))
    io_print(_func(u'c:\\21"'))
    io_print(_func(u'c:\\21|'))
    io_print(_func(u'c:\\21<'))
    io_print(_func(u'c:\\21>'))


def test_io_split_step():
    '''
    
    [(1, 2)]
    [(1, 2, 3, 4), (5, 6, 7)]
    [(1, 2, 3), (4, 5, 6), (7,)]

    '''
    cases = [
        ([1, 2], 5, [(1, 2)]),
        ([1, 2, 3, 4, 5, 6, 7], 4, [(1, 2, 3, 4), (5, 6, 7)]),
        ([1, 2, 3, 4, 5, 6, 7], 3, [(1, 2, 3), (4, 5, 6), (7,)])
    ]

    for e in cases:
        assert (list(io_iter_split_step(e[0], e[1])) == e[2])
        assert (list(_io_iter_split_step(e[0], e[1])) == e[2])

    print(u'pass {0}'.format(test_io_split_step.__name__))


def test():
    test_unicode_print()
    test_path()
    # test_io_is_path_valid()
    # test_io_split_step()


if __name__ == '__main__':
    test()
