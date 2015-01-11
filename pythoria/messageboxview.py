#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygcurse, pygame

pygame.font.init()

class MessageBoxView(pygcurse.PygcurseSurface):
    font = pygame.font.Font(pygame.font.match_font('consolas'), 14)
    
    def __init__(self, msgbox):
        super(MessageBoxView, self).__init__(40, 6, MessageBoxView.font)
        self.autoupdate = False
        self.msgbox = msgbox

    def draw(self):
        self.setscreencolors()
        self.cursor = (0, 0)
        for msg in self.msgbox[:-1]:
            self.write(msg + '\n', fgcolor=(64, 64, 64))
        if self.msgbox:
            self.write(self.msgbox[-1])
        self.update()
