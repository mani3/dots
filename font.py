#!/usr/bin/env python
# coding:utf-8


class Glyph:
    char = 0
    encoding = 0
    swidth = []
    dwidth = []
    bbx = []
    bitmap = []

    def __init__(self, char):
        self.char = char

    def __repr__(self):
        return '<{0}({1}, {2})>'.format(
            self.__class__.__name__, self.encoding, self.bitmap)


class BDF:
    version = ''
    font = ''
    size = []
    bounding_box = []
    properties = {}

    count = 0
    chars = []

    def __init__(self, f):
        stack_properties = None
        glyph = None
        bitmap = []
        for line in f:
            row = line.rstrip().split(' ')
            key = row[0]
            values = row[1:]
            if key == 'STARTFONT':
                self.version = values[0]
            elif key == 'FONT':
                self.font = values[0]
            elif key == 'SIZE':
                self.size = values
            elif key == 'FONTBOUNDINGBOX':
                self.bounding_box = values
            elif key == 'STARTPROPERTIES':
                stack_properties = {}
            elif key == 'ENDPROPERTIES':
                self.properties = stack_properties
                stack_properties = None
            elif key == 'CHARS':
                self.count = int(values[0])
            elif key == 'STARTCHAR':
                glyph = Glyph(int(values[0], 16))
            elif key == 'ENCODING':
                if glyph is not None:
                    glyph.encoding = int(values[0])
            elif key == 'SWIDTH':
                if glyph is not None:
                    glyph.swidth = values
            elif key == 'DWIDTH':
                if glyph is not None:
                    glyph.dwidth = values
            elif key == 'BBX':
                if glyph is not None:
                    glyph.bbx = values
            elif key == 'BITMAP':
                bitmap = []
            elif key == 'ENDCHAR':
                glyph.bitmap = bitmap
                self.chars.append(glyph)
                glyph = None
                bitmap = None
            else:
                if stack_properties is not None:
                    stack_properties[key] = values[0]
                if bitmap is not None:
                    bitmap.append(key)

    def bitmap(self, decimal):
        for c in self.chars:
            if c.encoding == decimal:
                return c.bitmap
        return None
