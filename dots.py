#!/usr/bin/env python
# coding:utf-8

import sys
import binascii
from jis import JIS
from font import BDF


def dots(char='', pixel='＠', space='　'):
    filename = 'misaki_gothic.bdf'
    bdf = None
    jis = JIS()

    with open(filename, 'r') as f:
        bdf = BDF(f)

    b = binascii.hexlify(char.encode('shift-jis'))
    shift_jis_code = hex(int(b, 16))
    try:
        jis_code = int(jis.code[shift_jis_code], 16)
        bitmap = bdf.bitmap(jis_code)
        dots = ''
        for b in bitmap:
            line = bin(int(b, 16))[2:].zfill(8)
            line = line.replace('0', space)
            line = line.replace('1', pixel)
            dots += line + '\n'
        return dots
    except KeyError:
        return 'Not found character code: "{0}"'.format(char)
    except TypeError:
        return 'Not found bitmap: "{0}"({1})'.format(char, jis_code)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        pixel = '＠'
        space = '　'
        for c in args[0]:
            glyph = dots(c, pixel=pixel, space=space)
            print(glyph)
    else:
        print('Usage: {0} <text> <pixel> <space>'.format(sys.argv[0]))
        exit(-1)
