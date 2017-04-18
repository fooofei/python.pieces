
## python -m 运行一个 .py 文件

目录结构

```
$ tree 1
1
├── package1
│   ├── __init__.py
│   └── mod1.py
└── package2
    ├── __init__.py
    └── run.py

2 directories, 4 files

```

package1/\_\_init\_\_.py
```
```
package1/mod1.py
```python
#coding=utf-8


def func_mod1():
    print ('from {}'.format(func_mod1.__name__))
```

package2/\_\_init\_\_.py
```
```

package2/run.py
```python
#coding=utf-8

from package1 import mod1

def entry():
    mod1.func_mod1()

    print ('from {}'.format(entry.__name__))


if __name__ == '__main__':
    entry()
```



### 在 1 目录执行 `python package2/run.py`

```
$ python package2/run.py 
Traceback (most recent call last):
  File "package2/run.py", line 3, in <module>
    from package1 import mod1
ImportError: No module named package1
```

### 在 1/package2 目录执行 `python run.py`

```
$ python run.py 
Traceback (most recent call last):
  File "run.py", line 3, in <module>
    from package1 import mod1
ImportError: No module named package1
```

### 在 1 目录执行 `python -m package2.run`
```
$ python -m package2.run
from func_mod1
from entry
```


### 在 1/package2 目录执行 `python -m run`
```
$ python -m run   
Traceback (most recent call last):
  File "/usr/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/usr/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/media/sf_F_DRIVE/everysamples/0000/bbs/1/package2/run.py", line 3, in <module>
    from package1 import mod1
ImportError: No module named package1
```