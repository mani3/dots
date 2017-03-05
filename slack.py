#!/usr/bin/env python
# coding:utf-8

import time
import re
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
                    try:
                        m = re.search(r'『(.*)』', text)
                        message = m.group(1)
                        emojis = re.findall('\:\w+?\:', text)
                        pixel = safe(emojis, 0, ':black:')
                        space = safe(emojis, 1, ':white:')
                        post(slack, message, pixel, space, channel)
                    except Exception:
                        pass
            time.sleep(1)
    else:
        print('Connection Failed, invalid token?')


if __name__ == '__main__':
    main()
