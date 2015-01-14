#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygcurse, pygame

pygame.font.init()

class HUDView(pygcurse.PygcurseSurface):
    font = pygame.font.Font(pygame.font.match_font('consolas'), 18)

    def __init__(self, player):
        self.player = player
        super(HUDView, self).__init__(30, 30, HUDView.font)
        self.autoupdate = False

    def draw(self):
        self.setscreencolors(clear=True)
        self.cursor = (0, 0)
        self.putchars("Player")
        self.putchars("x={:<4}".format(self.player.x), x=2, y=1)
        self.putchars("y={:<4}".format(self.player.y), x=2, y=2)
        self.update()
