#!/usr/bin/env python
# coding:utf-8

import os
import urllib.request
import csv


JIS_URL = 'http://www.unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0208.TXT'
JIS_FILE = os.path.basename(JIS_URL)


class JIS:
    code = {}

    def __init__(self):
        if os.path.exists(JIS_FILE) is False:
            self.download()
        self.code = self.load()

    def download(self, url=JIS_URL):
        res = urllib.request.urlopen(url)
        with open(os.path.basename(url), 'wb') as f:
            f.write(res.read())

    def load(self, filename=JIS_FILE):
        jis = {}
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader)
            for row in reader:
                if not row[0].startswith('#'):
                    jis[row[0].lower()] = row[1].lower()
        return jis
