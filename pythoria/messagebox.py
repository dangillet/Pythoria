#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

class MessageBox(list):
    def __init__(self, *msgs):
        super(MessageBox, self).__init__(msgs)

    def add(self, msg):
        date = datetime.datetime.now().strftime('[%H:%M:%S] ')
        self.append(date + msg)

    def __str__(self):
        return '\n'.join(self)