
### hadoop mr 的参数顺序
bin/hadoop command [genericOptions] [commandOptions]
先有 genericOptions， 再有 commandOptions，参数顺序不能反 
Generic options supported are
-conf <configuration file>  
-D <property=value>          
-fs <local|namenode:port>    
-jt <local|jobtracker:port>   
-jtold <local|jobtracker:port>   
-files <comma separated list of files>   
-libjars <comma separated list of jars>    
-archives <comma separated list of archives>   



### streaming official doc
https://hadoop.apache.org/docs/r1.0.4/cn/streaming.html



mr 流程 
Map -> Combiner -> Partitioner -> Sort -> Shuffle -> Sort -> Reduce
https://community.hortonworks.com/questions/14328/what-is-the-difference-between-partitioner-combine.html

Reducer have 3 parts ：shuffle, sort, reduce.
see http://hadoop.apache.org/docs/r1.0.4/cn/mapred_tutorial.html
see https://stackoverflow.com/questions/11672676/when-do-reduce-tasks-start-in-hadoop

In my words, mapreduce contains map-->shuffle-->sort-->reduce 4 stages, the process of 
the web backend shows map->reduce only, not contains shuffle/sort.
the shuffle and sort stage is show in reduce stage, the reduce contains shuffle-->sort-->reduce,
generally the reduce starts when all maps finish, but in the web backend shows, the mapper not all
finished and the reduce start, so that is the shuffle stage, the shuffle stage start not wait all
maps finish, but the sort is waiting all maps finish, so if the maps not all finish, the reduce will
show stop at 33%, it is the shuffle stage process.



KeyFieldBasePartitioner 跟排序相关



'-D', 'mapred.output.compress=true',
'-D', 'mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec',
设置 mr 的输出为 gz 压缩过的, -D 是 genericOptions



-D -jobconf 都可以用作指定配置，但 -D 是通用的，-jobconf 仅仅对 streaming 程序使用



### 几个上传压缩包的方法
文件打包上传方法(HDFS 缓存文件上传)，mr 自动解压，访问这个目录使用 .pypy, 末尾 #pypy 的意思是解压到 pypy 名字的目录

'-cacheArchive', '/home/share/pypy.tar.gz#pypy',
这个会报警告：
WARN streaming.StreamJob: -cacheArchive option is deprecated, 
please use -archives instead.

'-archives', '/home/share/pypy.tar.gz#pypy',
注意到 archives is genericOptions
但是很奇怪，直接把 cacheArchive 替换为 archives 会异常，运行错误：
```
sh: ./pypy/bin/pypy: (接下来是乱码)
run_cmd failed: 127
java.lang.RuntimeException: PipeMapRed.waitOutputThreads(): 
subprocess failed with code 127
```
可能是不支持软连接，以后不要用这个

'-D', 'mapred.cache.archives=/home/share/pypy-5.8-linux_x86_64-portable.tar.gz#pypy',
这个好用



'-files', 'libqexpy',
多文件(本地文件)(目录)（用作模块的 py 文件）上传方法



-D mapred.reduce.tasks=0
-reducer NONE
不使用 reducer



'-D', 'mapred.ignore.badcompress=true', 
在 MapReduce 处理过程中忽略压缩损坏的文件



'-D', 'mapred.input.dir.recursive=true',
批量输入目录的方式：
https://stackoverflow.com/questions/26647946/how-recursively-use-a-directory-structure-in-the-new-hadoop-api
可以支持在输入路径中递归匹配各级目录中的文件。
如：输入路径为：
/home/mr/wuyunyun/input-dir1/sub-dir1/file1,
/home/mr/wuyunyun/input-dir1/sub-dir2/file2,
则可设置此参数为true，
给定输入-input /home/mr/wuyunyun/input-dir1/
即可匹配input-dir1中子目录中的文件



'-D', 'mapred.input.dir.error.pass=true',
批量输入目录的方式：input 输入目录中存在 match=0 时 也忽略



'-outputformat', 'org.apache.hadoop.mapred.lib.SuffixMultipleTextOutputFormat',
'-D', 'suffix.multiple.outputformat.filesuffix=hbase_import,exceptions,tables',
'-D', 'suffix.multiple.outputformat.separator=#',
多路输出
注：map reduce 输出时,
当value为空时要在key值与"suffix.multiple.outputformat.separator"之间补充一个"\t"分隔符
不然失败



### portable pypy for mapreduce

download from  https://github.com/squeaky-pl/portable-pypy


一个短篇：批量输入目录的两种方式
要输入 /home/day=201609 一个月内所有日志，可以有：
1 '-D', 'mapred.input.dir.recursive=true', 设置递归，然后 input=/home/day=201609* 即可，
中间某一天目录为空，没有输入也会被忽略。

2 '-D', 'mapred.input.dir.error.pass=true', 设置忽略某天输入日志为空的情况，
input=/home/day=20160901/*,
/home/day=20160902/*,
/home/day=20160903/*,
/home/day=20160904/*,
/home/day=20160905/*,
/home/day=20160906/*,
/home/day=20160907/*,
/home/day=20160908/*,
/home/day=20160909/*,
/home/day=20160910/*,
/home/day=20160911/*,
/home/day=20160912/*,
/home/day=20160913/*,
/home/day=20160914/*,
/home/day=20160915/*,
/home/day=20160916/*,
/home/day=20160917/*,
/home/day=20160918/*,
/home/day=20160919/*,
/home/day=20160920/*,
/home/day=20160921/*,
/home/day=20160922/*,
/home/day=20160923/*,
/home/day=20160924/*,
/home/day=20160925/*,
/home/day=20160926/*,
/home/day=20160927/*,
/home/day=20160928/*,
/home/day=20160929/*,
/home/day=20160930/*

或者简写
-s=/home/day=201609[0-9][0-9]/*