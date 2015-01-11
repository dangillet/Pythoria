#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class HUDView:
    def __init__(self, player, win):
        self.player = player
        self.win = win

    def draw(self, x, y):
        self.win.putchars("Player", x=x, y=y, indent=True)
        self.win.putchars("x={}".format(self.player.x), x=x+2, y=y+1, indent=True)
        self.win.putchars("y={}".format(self.player.y), x=x+2, y=y+2, indent=True)