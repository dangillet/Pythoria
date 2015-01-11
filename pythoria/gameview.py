#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygcurse, pygame

class GameView:
    def __init__(self, win, views):
        self.win = win
        self.views = views

    def draw(self):
        for view, coords in self.views.items():
            view.draw()
            view.blitto(self.win.surface, dest=coords)
