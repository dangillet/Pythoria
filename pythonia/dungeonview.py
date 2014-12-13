#!/usr/env/ python
#-*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import pygcurse, pygame
from dungeon import Map

PLAYER = '\N{WHITE SMILING FACE}' # Unicode for a smile

class DungeonView(object):
    def __init__(self, dungeon, win):
        self.dungeon = dungeon
        self.win = win
        self.win.font = pygame.font.Font('C:\Windows\Fonts\Consola.ttf', 22)
        
    def draw(self):
        "Draw the dungeon and the player."

        for line in self.dungeon:
            self.win.write(line)
            self.win.write('\n')
        self.win.putchar(PLAYER, x=self.dungeon.player.x, y=self.dungeon.player.y)

if __name__ == '__main__':
    import dungeon
    win = pygcurse.PygcurseWindow(40,30)
    level1 = Map.load_from_file('../test/map.txt')
    view = DungeonView(level1, win)
    view.draw()
    pygcurse.waitforkeypress()
