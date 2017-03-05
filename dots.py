#!/usr/bin/env python
# coding:utf-8

import os
import sys
import urllib.request
import tarfile
import binascii
from jis import JIS
from font import BDF

MISAKI_FONT_URL = 'http://www.geocities.jp/littlimi/arc/misaki/misaki_bdf_2012-06-03.tar.gz'
MISAKI_BDF = 'misaki_gothic.bdf'
MISAKI_FILE = os.path.basename(MISAKI_FONT_URL)

def download_font(url):
    if os.path.exists(MISAKI_FILE) is False:
        res = urllib.request.urlopen(url)
        with open(os.path.basename(url), 'wb') as f:
            f.write(res.read())
    if os.path.exists(MISAKI_BDF) is False:
        tar = tarfile.open(MISAKI_FILE)
        tar.extractall()
        tar.close()


def dots(char='', pixel='＠', space='　'):
    download_font(MISAKI_FONT_URL)

    # filename = 'milkjf_k16.bdf'
    filename = MISAKI_BDF
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
            line = bin(int(b, 16))[2:].zfill(len(b)*4)
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
