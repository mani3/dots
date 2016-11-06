#!/usr/bin/env python
# coding:utf-8

import time
from slackclient import SlackClient
from dots import dots


API_TOKEN = ''
CHANNEL = '#general'


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
