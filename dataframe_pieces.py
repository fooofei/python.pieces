# coding=utf-8

import os
import sys

curpath = os.path.dirname(os.path.realpath(__file__))

data = '''\
111\taaa
111\tbbb
222\tccc
333\tddd
'''

column_names = ['column_0', 'column_1']

import pandas as pd
from cStringIO import StringIO


def make_gzip():
    import gzip

    out_stream = StringIO()

    with gzip.GzipFile(fileobj=out_stream, mode='wb') as f:
        f.write(data)
    return StringIO(out_stream.getvalue())


def creat_base():
    '''
   column_0 column_1
0       111      aaa
1       111      bbb
2       222      ccc
3       333      ddd

    :return: 
    '''
    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    return chunk


def read_from_gzip():
    '''
   column_0 column_1
0       111      aaa
1       111      bbb
2       222      ccc
3       333      ddd
    '''
    chunk = pd.read_csv(make_gzip(),
                        names=column_names,
                        header=None,
                        sep='\t',
                        compression='gzip',  # default 'infer' 如果是文件路径，从文件后缀推断
                        # engine='python',  #  python or c
                        )
    return chunk


def drop_duplicates():
    '''
   column_0 column_1
0       111      aaa
2       222      ccc
3       333      ddd
    :return: 
    '''

    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    chunk2 = chunk.drop_duplicates(column_names[0])

    return chunk2


def drop_nan():
    local_data = '''\
111\taaa
222\t
333\tccc
'''

    stream = StringIO(local_data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    '''
       column_0 column_1
0       111      aaa
1       222      NaN
2       333      ccc
    :return: 
    '''

    chunk2 = chunk[pd.notnull(chunk[column_names[1]])]

    '''
   column_0 column_1
0       111      aaa
2       333      ccc
    '''

    return chunk2


def drop_columns():
    '''
       column_0
0       111
1       111
2       222
3       333
    :return: 
    '''
    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    chunk2 = chunk.drop(chunk.columns[[1]], axis=1)

    return chunk2


def concat_with_same_columns():
    '''
       column_0 column_1
0       111      aaa
1       111      bbb
2       222      ccc
3       333      ddd
0       111      aaa
1       111      bbb
2       222      ccc
3       333      ddd
    :return: 
    '''
    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    chunk2 = pd.concat([chunk, chunk])

    return chunk2


def concat_with_different_columns():
    '''
       column_0  column_00 column_1 column_11
0     111.0        NaN      aaa       NaN
1     111.0        NaN      bbb       NaN
2     222.0        NaN      ccc       NaN
3     333.0        NaN      ddd       NaN
0       NaN      111.0      NaN       aaa
1       NaN      111.0      NaN       bbb
2       NaN      222.0      NaN       ccc
3       NaN      333.0      NaN       ddd
    :return: 
    '''
    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    stream.seek(0)
    chunk1 = pd.read_csv(stream,
                         names=['column_00', 'column_11'],
                         header=None,
                         sep='\t')

    chunk2 = pd.concat([chunk, chunk1])

    return chunk2


def sort_by():
    local_data = '''\
111\tccc
444\taaa
333\tbbb
'''

    stream = StringIO(local_data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    chunk1 = chunk.sort_values(by=[column_names[0]])
    '''
       column_0 column_1
0       111      ccc
2       333      bbb
1       444      aaa
    '''

    chunk2 = chunk.sort_values(by=[column_names[1]])
    '''
       column_0 column_1
1       444      aaa
2       333      bbb
0       111      ccc
    '''
    return chunk1


def save_to_file():
    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    fullpath = os.path.join(curpath, 'test.bin')
    if os.path.exists(fullpath):
        os.remove(fullpath)
    chunk.to_csv(fullpath,
                 sep='\t',
                 index=False,
                 header=False,
                 )

    '''
111	aaa
111	bbb
222	ccc
333	ddd

    '''

    return 'save_to_file {}'.format(fullpath)


def special_handle_columns_when_create():
    '''
    此函数演示在创建 dataframe 时特殊处理列
    
          column_0 column_1
0  111_convert      aaa
1  111_convert      bbb
2  222_convert      ccc
3  333_convert      ddd
    :return: 
    '''

    def func_convert(text):
        try:
            return text + '_convert'
        except AttributeError:
            return text

    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t',
                        converters={column_names[0]: func_convert},  # 指定这一列使用什么函数转换
                        )

    return chunk


def to_list():
    '''
    [   {'column_1': 'aaa', 'column_0': 111}, 
        {'column_1': 'bbb', 'column_0': 111}, 
        {'column_1': 'ccc', 'column_0': 222}, 
        {'column_1': 'ddd', 'column_0': 333}
        ]
        
    '''

    def pandas_dataframe_to_list(df):
        r = []
        for k in df.itertuples():
            e = {}
            for n in df.columns.values:
                e[n] = getattr(k, n)
            r.append(e)
        return r

    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    return pandas_dataframe_to_list(chunk)


def column_to_list():
    '''
    ['aaa', 'bbb', 'ccc', 'ddd']
    :return: 
    '''
    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    return chunk[column_names[1]].tolist()


def read_column_names():
    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    # or  list(chunk)
    return chunk.columns.values


def only_read_column():
    '''
    该函数演示按列访问 DataFrame
    :return: 
    '''
    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    for e in chunk.iteritems():
        print (e)


def column_name_to_column_index():
    '''
    colum_name column_1 is index 1
    :return: 
    '''
    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    return 'colum_name {} is index {}'.format(
        column_names[1],
        chunk.columns.get_loc(column_names[1])
    )


def update_specific_value():
    '''
       column_0 column_1
0       111      aaa
1       111      eee
2       222      ccc
3       333      ddd
    :return: 
    '''
    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    for index, row in chunk.iterrows():
        if row[column_names[1]] == 'bbb':
            chunk.set_value(index, column_names[1], 'eee')

    return chunk


def insert_new_column():
    '''
       column_0 column_1 column_new_insert
0       111      aaa     default_value
1       111      bbb     default_value
2       222      ccc     default_value
3       333      ddd     default_value
    :return: 
    '''

    stream = StringIO(data)

    chunk = pd.read_csv(stream,
                        names=column_names,
                        header=None,
                        sep='\t')

    names = chunk.columns.values
    last_name_index = chunk.columns.get_loc(names[-1])
    chunk.insert(last_name_index + 1, 'column_new_insert', 'default_value')

    return chunk


def entry():
    funcs = [
        creat_base,
        read_from_gzip,
        drop_duplicates,
        drop_nan,
        drop_columns,
        concat_with_same_columns,
        concat_with_different_columns,
        sort_by,
        # save_to_file,
        special_handle_columns_when_create,
        read_column_names,
        column_to_list,
        to_list,
        column_name_to_column_index,
        update_specific_value,
        insert_new_column,
    ]

    for e in funcs:
        print (e())


if __name__ == '__main__':
    entry()
