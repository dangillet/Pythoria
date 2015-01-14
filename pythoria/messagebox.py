#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textwrap


class MessageBox(list):
    def __init__(self, width=18, height=5, *msgs):
        self.wrapper = textwrap.TextWrapper(width=width)
        super(MessageBox, self).__init__(map(self.wrapper.fill, msgs))
        self.width, self.height = width, height

    def add(self, msg):
        import datetime
        date = datetime.datetime.now().strftime('[%H:%M:%S] ')
        self.append(self.wrapper.fill(date + msg))

    def __str__(self):
        return '\n'.join(self)