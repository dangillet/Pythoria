#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygcurse, pygame

class MessageBoxView(pygcurse.PygcurseSurface):
    font = pygame.font.Font(pygame.font.match_font('consolas'), 14)
    
    def __init__(self, msgbox):
        super(MessageBoxView, self).__init__(80, 5, MessageBoxView.font)
        self.autoupdate = False
        self.msgbox = msgbox

    def draw(self):
        self.setscreencolors()
        self.cursor = (0, 0)
        for msg in self.msgbox[-self.msgbox.height:]:
            self.write(msg + '\n')
        self.update()
