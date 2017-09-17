# coding=utf8

'''
该文件研究路径编码对 ctypes LoadLibrary 的影响
'''

import os
import sys
import ctypes

if os.name in ('nt', 'ce'):
    from ctypes import WINFUNCTYPE as ExportFuncType
    from ctypes import windll as library_loader
else:
    from ctypes import CFUNCTYPE as ExportFuncType
    from ctypes import cdll as library_loader


def entry():
    '''
    1 在 Windows Python 2.7.13 测试 LoadLibrary 只接受 bytes string 参数，不接受 unicode string.

    2 一个字符串编码转换测试背景:
    一个 unicode string 中文路径，被 .encode('utf-8') ，
    Windows 上 os.path.exists 会 return False
    是因为 Windows AwPI char 使用的是 (ANSI)GB18030 ，linux 使用的是 utf-8

    3 Windows API 和 linux API char 的编码不同，验证过程是 ：

    Windows (代码中硬编码 + 使用 os.walk 遍历到的) 一个 unicode string 中文路径
    --> .encode('utf-8') ->LoadLibrary  error
    Windows (代码中硬编码 + 使用 os.walk 遍历到的) 一个 unicode string 中文路径
    --> .encode('gb18030') ->LoadLibrary  success

    linux (代码中硬编码 + 使用 os.walk 遍历到的) 一个 unicode string 中文路径
    --> .encode('utf-8') ->LoadLibrary  success
    linux (代码中硬编码 + 使用 os.walk 遍历到的) 一个 unicode string 中文路径
    --> .encode('gb18030') ->LoadLibrary  error

    4 查看 windows python2 的 c语言源码发现，即便是 python 语言和 Windows API
      都支持 unicode，但 python 依旧是参数接受 char, 假如使用 Windows Unicode
      *W API，还要 MultiByteToWideChar(CP_ACP,...) 转为 unicode，增加负担。

    5 在 python2, python3 中，相关源代码有：
    py2 https://svn.python.org/projects/python/trunk/Modules/_ctypes/callproc.c
    该源码是经过 fix 的版本，与下载到的 python 2.7.13 源码不一致
    相关 bug issue 地址 http://bugs.python.org/issue29294  http://bugs.python.org/issue29082

    static PyObject *load_library(PyObject *self, PyObject *args)
    {
        TCHAR *name;
        PyObject *nameobj;
        PyObject *ignored;
        HMODULE hMod;
        if (!PyArg_ParseTuple(args, "O|O:LoadLibrary", &nameobj, &ignored))
            return NULL;
    #ifdef _UNICODE
        name = alloca((PyString_Size(nameobj) + 1) * sizeof(WCHAR));
        if (!name) {
            PyErr_NoMemory();
            return NULL;
        }

        {
            int r;
            char *aname = PyString_AsString(nameobj);
            if(!aname)
                return NULL;
            r = MultiByteToWideChar(CP_ACP, 0, aname, -1, name, PyString_Size(nameobj) + 1);
            name[r] = 0;
        }
    #else
        name = PyString_AsString(nameobj);
        if(!name)
            return NULL;
    #endif

        hMod = LoadLibrary(name);
        if (!hMod)
            return PyErr_SetFromWindowsErr(GetLastError());
    #ifdef _WIN64
        return PyLong_FromVoidPtr(hMod);
    #else
        return Py_BuildValue("i", hMod);
    #endif
    }

    py3 https://github.com/python/cpython/blob/master/Modules/_ctypes/callproc.c#L1250

    static PyObject *load_library(PyObject *self, PyObject *args)
    {
        const WCHAR *name;
        PyObject *nameobj;
        PyObject *ignored;
        HMODULE hMod;

        if (!PyArg_ParseTuple(args, "U|O:LoadLibrary", &nameobj, &ignored))
            return NULL;

        name = _PyUnicode_AsUnicode(nameobj);
        if (!name)
            return NULL;

        hMod = LoadLibraryW(name);
        if (!hMod)
            return PyErr_SetFromWindowsErr(GetLastError());
    #ifdef _WIN64
        return PyLong_FromVoidPtr(hMod);
    #else
        return Py_BuildValue("i", hMod);
    #endif
    }


    '''
    name = u''
    library_loader.LoadLibrary(name)


if __name__ == '__main__':
    entry()
