# coding=utf-8
'''
the file shows how to use ida'dif file to patch a file

dif file like :
This difference file has been created by IDA

010Editor.bk.exe
00FBD626: 83 90
00FBD627: 7E 90
00FBD628: 2C 90
00FBD629: 00 90
00FBD62A: 74 90
00FBD62B: 0A 90
00FBD62D: 13 DB
00FBD62E: 01 00


'''
import os
import sys
import re


def ida_dif_patcher(binary_fullpath, dif_fullpath):
    code = bytearray(os.path.getsize(binary_fullpath))
    with open(binary_fullpath, 'rb') as fr:
        fr.readinto(code)

    patcher_fullpath = binary_fullpath + u'_patcher'
    if os.path.exists(patcher_fullpath): os.remove(patcher_fullpath)

    with open(dif_fullpath, 'r') as fr:
        fr.next()  # skip 'This difference file...'
        fr.next()  # skip empty line
        fr.next()  # skip binary name
        for l in fr:
            l = l.rstrip()
            dif1 = re.findall('([0-9a-fA-F]+): ([0-9a-fA-F]+) ([0-9a-fA-F]+)', l)
            assert (len(dif1) == 1)
            offset, original, patch1 = dif1[0]
            offset = int(offset, 16)
            original = int(original, 16)
            patch1 = int(patch1, 16)

            if code[offset] != original:
                raise ValueError('patch not right offset={} '
                                 'original={} code[offset]={}'.format(offset, original, code[offset]))

            code[offset] = patch1

    with open(patcher_fullpath, 'wb') as fw:
        fw.write(code)


if __name__ == '__main__':
    ida_dif_patcher(sys.argv[1], sys.argv[2])
