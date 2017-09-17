# coding=utf-8

'''
the file shows how to use xml's header encoding to decode a xml

服务器返回的数据有时候是 xml, 在头部 encoding 标记为 utf-8 外的其他编码，
现有的 xml 解析库默认都是以 utf-8 解码，即使把编码用参数传递，但是无法做到
自动取用 xml 中记载的编码

但是我们要根据 xml 头中的编码来解码整个文本。

下面的函数就是一段 xml 文本中读取头部，获取应该使用的编码。

'''

import os
import sys
import unittest

def _get_encoding_from_xml_header(xml_content):
    '''
     ref   https://stackoverflow.com/questions/25796238/reading-xml-header-encoding

     仅仅使用
        p = expat.ParserCreate()
        p.XmlDeclHandler = a._f
        r = p.Parse(xml_content,1)
     解析 xml 头 也报错 ValueError: multi-byte encodings are not supported 没办法用

     下面的代码内部使用的 expat
    '''

    class _xml_header_descriptor(object):
        def _f(self, *args, **kwargs):
            self._args = args

    import xml.etree.ElementTree  as ET
    xmlp = ET.XMLParser(encoding='utf-8')
    desp = _xml_header_descriptor()
    xmlp.parser.XmlDeclHandler = desp._f

    if not xml_content.startswith('<?'): return None
    index_header_end = xml_content.find('?>')
    if index_header_end == -1: return None
    xml_content = xml_content[:index_header_end + 2:]

    # 必须有一个标签 加一个 <end> 伪装
    f = ET.fromstring(xml_content + '<end></end>', parser=xmlp)
    version, encoding, standalong = desp._args
    return encoding



class MyTestCase(unittest.TestCase):

    def test_get_encoding(self):
        a = '<?xml version="1.0" encoding="GBK" ?>'

        self.assertEqual(_get_encoding_from_xml_header(a),'GBK')


if __name__ == '__main__':
    unittest.main()