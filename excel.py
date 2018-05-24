#coding=utf-8

'''
before run, you need to execute

$ pip install xlutils
$ pip install pandas
$ pip install xlrd
$ pip install xlwt

进展：
xlwt 只能创建 xls 不能打开已经存在的文件并且修改
xlrd 能读取 xls
openpyxl 只能处理 xlsx 更新的office 类型 不支持 xls

为了读写同时进行 需要在这两个类型中间转换
    (Pdb) p type(writer.book)
    <class 'xlwt.Workbook.Workbook'>
    (Pdb) p type(book)
    <class 'xlrd.book.Book'>
目前还没成功

https://stackoverflow.com/questions/26957831/edit-existing-excel-workbooks-and-sheets-with-xlrd-and-xlwt

'''

import os
import sys

import datetime
import pandas
import pdb
import xlrd
import xlutils.copy as xlcopy



def entry():
    fullpath=r'C:\Users\Desktop\1.xls'
    fexcel = pandas.read_excel(fullpath, names=['esn','name','type','site','detail'],skiprows=2,sheet_name=u'导入设备列表')

    sheets={}

    #site_index = fexcel.columns.get_loc('site')
    for row in fexcel.iterrows():
        # row[0] is row index, 0, 1, 2
        v = sheets.setdefault(row[1]['site'], [])
        v.append(row[1])

    rbook = xlrd.open_workbook(fullpath,formatting_info=True) # <class 'xlrd.book.Book'>
    # formatting_info 带着格式复制

    wbook = xlcopy.copy(rbook) # <class 'xlwt.Workbook.Workbook'>

   # writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    with pandas.ExcelWriter(fullpath)as writer:
        writer.book = wbook
        for k,v in sheets.iteritems():
            df = pandas.DataFrame(v)
            df.to_excel(writer,k, index=False,header=[u'ESN',u'设备名称',u'设备型号',u'站点',u'描述'])
        writer.save()


    print('done')

def writer_test():
    ''' 这个只能在新的文件上加 sheet ，不能先读取然后做修改 '''
    fullpath=r'C:\Users\Desktop\1.xls'
    writer = pandas.ExcelWriter(fullpath)

    book = writer.book
    sheet1 = book.add_sheet('1')

    writer.save()

if __name__ == '__main__':
    entry()
