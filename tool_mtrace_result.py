#coding=utf-8

# ref https://github.com/fooofei/cpp_notes/blob/master/memory_leak.md

def read_mtrace_result():
    fullpath = ''
    mhash={}
    with open(fullpath, 'rb') as fr:
        for line in fr:
            if line.startswith('0x'):
                fields = line.split(' ')
                # 过滤掉纯空格的
                fields = filter(lambda x: x, fields)
                if len(fields) == 4:
                    size = fields[1]
                    size= int(size,16)
                    key = fields[-1]
                    key = key.rstrip()
                    mhash.setdefault(key,0)
                    mhash[key] += size



    keys = sorted(mhash, key=mhash.get, reverse=True)
    print('keys count = {c}'.format(c=len(keys)))

    for key in keys:
        print('{k} {v}'.format(k=key, v=mhash.get(key)))



if __name__ == '__main__':
    read_mtrace_result()
