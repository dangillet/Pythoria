#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MessageBoxView:
    def __init__(self, msgbox, win):
        self.win = win
        self.msgbox = msgbox

    def draw(self, x, y):
        for y_offset, msg in enumerate(self.msgbox[-3:]):
            self.win.putchars(msg, x=x, y=y+y_offset)