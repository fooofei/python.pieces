#coding=utf-8
'''
 尝试寻找一种方式 把某个脚本文件及其依赖的其他脚本文件打包为
 一个 zip 文件，让 python 直接运行这个 zip 文件
 因为 zip 文件在不同机器之间可移动性强

历程

    20180327
        python 3.5 https://docs.python.org/3/library/zipapp.html
        有 zipapp 模块可以使用 低版本的没有
        python3 -m zipapp --python "/usr/bin/env python" --output <>\aa.pyz <source_dir>
        成了
        加 --main 都不成
        入口文件 要重命名为 __main__.py
        不能自动关联 __main__.py import 了一个第三方库， 如果不放在这个 <source_dir>
          里就不会被压缩 生成的文件就不能运行

    这里有一个适用于 python 2.7 的
        http://www.evanjones.ca/software/packagepy.html
        这个代码的 notBuiltInModules 寻找非内建模块有缺陷 把内建模块也包含进去
        我做了修改

    https://github.com/BTOdell/pyz
        还不知道怎么使用这个库

    后来我自己压缩自己
    找好 curpath

        # If run by .py file, the
        #   curpath =     <dir>/pycore.py
        #   sys.path[0] = <dir>
        # If run by .pyz file, the
        #   curpath = <dir>/pycore.pyz/__main__.py
        #   sys.path[0] = pycore.pyz
        this_execfile_fullpath = os.path.realpath(__file__)
        this_file_name =os.path.basename(this_execfile_fullpath)
        parent_dirname= os.path.basename(os.path.dirname(this_execfile_fullpath))
        if (this_file_name=='__main__.py'
            and os.path.basename(sys.path[0]) == parent_dirname):
            this_execfile_fullpath = os.path.dirname(this_execfile_fullpath)
        this_file_dir = os.path.dirname(this_execfile_fullpath)

    cxfreeze 是把 .so 都拷贝出来
    这个脚本的使用方式 是把脚本导出为二进制运行
      python -m pip install cx_Freeze --upgrade
      $ cxfreeze pycore.py
      测试不适合这样使用 携带的文件太多了
      而且与平台绑定  python 的跨平台优势就没了

'''


def package_self_to_zip():
    import zipfile
    files=[
        (os.path.realpath(__file__),'__main__.py'),
        (os.path.join(this_file_dir,'a.py'),'a.py'),
    ]
    fullpath_pyz = os.path.join(this_file_dir,'pycore.pyz')
    if os.path.exists(fullpath_pyz):
        os.remove(fullpath_pyz)
    shebang = '#!/usr/bin/env python\n'
    with open(fullpath_pyz,'wb') as fw:
        fw.write(shebang)
        fw.flush()

    with zipfile.ZipFile(fullpath_pyz,'a',zipfile.ZIP_DEFLATED) as fwz:
        for source_path, relative_path in files:
            fwz.write(filename=source_path,arcname=relative_path)
    print('[+] Packaged self to {f}'.format(f=fullpath_pyz))


