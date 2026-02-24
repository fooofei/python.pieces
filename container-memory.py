#!/usr/bin/env python3
# coding=utf-8

# 这个文件演示了容器的内存如何计算


import errno
import os
import sys
import time

#
#   Functions
#

# The following matches "du -h" output
# see also human.py
def human(size_bytes, unit="Mi"):
    units = ["B", "Ki", "Mi", "Gi", "Ti"]

    for u in units:
        if u == unit:
            return "%.1f %sB" % (size_bytes, u)
        if size_bytes < 1000:
            return "%.1f %sB" % (size_bytes, u)
        size_bytes /= 1024.0


def read_file_mem_stat():
    '''
    parse file sample:
    cache 255467520
    rss 439832576
    rss_huge 379584512
    mapped_file 12496896
    swap 0
    pgpgin 121634
    pgpgout 1006076
    pgfault 137314
    pgmajfault 175
    inactive_anon 0
    active_anon 439771136
    inactive_file 55664640
    active_file 199802880
    unevictable 0
    hierarchical_memory_limit 6442450944
    hierarchical_memsw_limit 6442450944
    total_cache 255467520
    total_rss 439832576
    total_rss_huge 379584512
    total_mapped_file 12496896
    total_swap 0
    total_pgpgin 121634
    total_pgpgout 1006076
    total_pgfault 137314
    total_pgmajfault 175
    total_inactive_anon 0
    total_active_anon 439771136
    total_inactive_file 55664640
    total_active_file 199802880
    total_unevictable 0
    :return:
    '''
    fp = "/sys/fs/cgroup/memory/memory.stat"
    result = {}
    with open(fp, 'r') as fr:
        for line in fr:
            fields = line.splitlines()
            k = fields[0].strip()
            v = fields[1].strip()
            result[k] =v

    result["file"] = fp
    return result

def read_string_mem_stat():
    a = '''
cache 307687424
rss 40824832
rss_huge 0
mapped_file 13324288
swap 0
pgpgin 105626
pgpgout 22584
pgfault 38799
pgmajfault 171
inactive_anon 0
active_anon 40775680
inactive_file 68952064
active_file 238735360
unevictable 0
hierarchical_memory_limit 3221225472
hierarchical_memsw_limit 3221225472
total_cache 307687424
total_rss 40824832
total_rss_huge 0
total_mapped_file 13324288
total_swap 0
total_pgpgin 105626
total_pgpgout 22584
total_pgfault 38799
total_pgmajfault 171
total_inactive_anon 0
total_active_anon 40775680
total_inactive_file 68952064
total_active_file 238735360
total_unevictable 0
    '''
    result = {}
    for line in a.splitlines():
        fields = list(filter(lambda e: len(e) > 0 ,line.split(sep=" ")))
        if len(fields) < 2:
            continue
        k = fields[0].strip()
        v = int(fields[1].strip())
        result[k] = v
    return result


def mem_stats():
    '''
    容器内存

    container_memory_max_usage_bytes 
      > /sys/fs/cgroup/memory/memory.usage_in_bytes  = cAdvisor container_memory_usage_bytes
        >= （没有对应 cgroup 字段） container_memory_working_set_bytes = 执行kubectl top pod命令得到的结果(kubectl top pod <> --containers) 是容器真实使用的内存量，也是资源限制limit时的重启判断依据
          = 指标的组成实际上是 RSS + Cache  /sys/fs/cgroup/memory/memory.stat  rss 字段和 cache 字段
          = /sys/fs/cgroup/memory/memory.usage_in_bytes - (/sys/fs/cgroup/memory/memory.stat | grep total_inactive_file)
          > container_memory_rss
          这里有一个详细的图 https://blog.csdn.net/u010657094/article/details/138510248

    /sys/fs/cgroup/memory/memory.limit_in_bytes
    

    pod 内存
    /sys/fs/cgroup/memory/kubepods/burstable/podxxxx/memory.usage_in_bytes
    /sys/fs/cgroup/memory/kubepods/burstable/podxxxx/memory.stat

    go 语言
    go_memstats_heap_inuse_bytes > go_memstats_alloc_bytes
      原因： go_memstats_heap_inuse_bytes可能大于go_memstats_alloc_bytes，因为堆内存可能包含一些空闲的内存块，而这些内存块不被视为已分配的内存。
        此外，go_memstats_heap_inuse_bytes还包括了Go程序中使用的堆内存的开销，例如内存管理的元数据等，而go_memstats_alloc_bytes只包括了实际分配的内存量。
      所以说 alloc 叫分配，可能是对象的分配，元数据不算在这里面，但是在 inuse 里面
    使用 go_memstats_heap_inuse_bytes 更好 

    go_memstats_alloc_bytes  和 go_memstats_heap_alloc_bytes 是一致的

    go_memstats_heap_sys_bytes 
        不会降低，解释是
        当程序释放内存时，这些内存并不会立即返回给操作系统，而是被Go的内存池回收，以备后续使用。这意味着HeapSys的值不会因为内存释放而减少。

    go_memstats_alloc_bytes_total 不用分析
    go_memstats_stack_inuse_bytes 不用分析

    for file in /proc/*/status ; do awk '/VmSwap|Name/{printf $2 " " $3}END{ print ""}' $file; done | sort -k 2 -n -r | grep stress
    '''
    # cat /sys/fs/cgroup/memory/memory.usage_in_bytes
    usage_in_bytes = 348786688 #
    mstat = read_string_mem_stat()
    cache = mstat.get('cache',0) if mstat.get('cache',0) > 0 else mstat.get("total_cache",0)
    rss = mstat.get('rss',0) if mstat.get('rss',0) > 0 else mstat.get("total_rss",0)
    total_inactive_file =  mstat.get('total_inactive_file',0) if mstat.get('total_inactive_file',0) > 0 else mstat.get('inactive_file',0)

    print(f"cache size {human(cache)}")
    print(f"rss size {human(rss)}")
    print(f"total_inactive_file {human(total_inactive_file)}")
    print(f"limit_in_bytes {human(3221225472)}")

    # 第一个等式
    print(f"memory.usage_in_bytes size {human(usage_in_bytes)} usage=memory.stat rss+cache? // {human(rss+cache)}")

    #   Version:          18.09.0
    #   EulerVersion:     18.09.0.15
    #   Git commit:       f897bb1
    print(f"18.09.0.15 docker stats size {human(usage_in_bytes-cache)} {human(rss)}")
    #  Version:           18.09.0
    #  EulerVersion:      18.09.0.101
    #  Git commit:        384e3e9
    print(f"18.09.0.101 docker stats size working_set={human(usage_in_bytes - total_inactive_file)}")

    # kubectl top pod async-invoke-6797c7c5b5-4cxwg  --containers
    # 第二个等式 memory.usage_in_bytes = k8s kubelet working_set + memory.stat.total_inactive_file
    print(f"k8s kubelet working_set={human(usage_in_bytes - total_inactive_file)}")


    # 挖财是这样计算的 container_memory_usage_bytes - container_memory_cache
    # https://blog.opskumu.com/wacai-docker.html#orga8eee67

if __name__ == '__main__':
    mem_stats()




