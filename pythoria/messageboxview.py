#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygcurse, pygame
import textwrap

pygame.font.init()

class MessageBoxView(pygcurse.PygcurseSurface):
    font = pygame.font.Font(pygame.font.match_font('consolas'), 14)
    
    def __init__(self, msgbox, width=80, height=5):
        super(MessageBoxView, self).__init__(width, height, MessageBoxView.font)
        self.wrapper = textwrap.TextWrapper(width=width)
        self.width, self.height = width, height
        self.autoupdate = False
        self.msgbox = msgbox

    def draw(self):
        self.setscreencolors(clear=True)
        self.cursor = (0, 0)
        
        msgs = []
        for msg in self.msgbox[-self.height:]:
            splitted_msg = self.wrapper.wrap(msg)
            msgs.extend(splitted_msg)

        self.write('\n'.join(msgs[-self.height:]))
        self.update()
