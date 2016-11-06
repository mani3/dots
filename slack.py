#!/usr/bin/env python
# coding:utf-8

import time
import binascii
from slackclient import SlackClient
from jis import JIS
from font import BDF


API_TOKEN = ''
CHANNEL = '#general'


def dots(char='', pixel='＠', space='　'):
    filename = 'misaki_gothic.bdf'
    bdf = None
    jis = JIS()

    with open(filename, 'r') as f:
        bdf = BDF(f)

    b = binascii.hexlify(char.encode('shift-jis'))
    shift_jis_code = hex(int(b, 16))
    jis_code = int(jis.code[shift_jis_code], 16)
    bitmap = bdf.bitmap(jis_code)

    dots = ''
    for b in bitmap:
        line = bin(int(b, 16))[2:].zfill(8)
        line = line.replace('0', space)
        line = line.replace('1', pixel)
        dots += line + '\n'
    return dots


def post(slack, text='', pixel=':black_large_square:', space=':white_large_square:', channel=CHANNEL):
    for c in text:
        glyph = dots(c, pixel=pixel, space=space)
        slack.api_call(
            'chat.postMessage', username='dots',
            icon_emoji=':robot_face:', channel=channel, text=glyph)


def error(slack, channel=CHANNEL):
    msg = '''
    Usage: dots <message> <pixel> <space>
    '''
    slack.api_call(
        'chat.postMessage', username='dots',
        icon_emoji=':robot_face:', channel=channel, text=msg)


def safe(list, index, default=''):
    value = default
    try:
        value = list[index]
    except Exception:
        pass
    return value


def main():
    slack = SlackClient(API_TOKEN)
    if slack.rtm_connect():
        while True:
            for message in slack.rtm_read():
                text = message.get('text')
                channel = message.get('channel')
                if text is not None:
                    row = text.rstrip().split(' ')
                    try:
                        if row[0] == 'dots':
                            space = safe(row, 3, ':white_large_square:')
                            pixel = safe(row, 2, ':black_large_square:')
                            post(slack, row[1], pixel, space, channel)
                    except IndexError:
                        error(slack, channel)
            time.sleep(1)
    else:
        print('Connection Failed, invalid token?')


if __name__ == '__main__':
    main()
