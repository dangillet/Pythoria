#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division

import pygcurse, pygame
from dungeon import Dungeon

PLAYER = '\N{WHITE SMILING FACE}' # Unicode for a smile

class DungeonView(object):
    
    def __init__(self, dungeon, win):
        self.dungeon = dungeon
        self.win = win
        self.win.font = pygame.font.Font('C:\Windows\Fonts\Consola.ttf', 22)
        
    def draw(self):
        "Draw the dungeon and the player."
        
        for line in self.dungeon:
            for tile in line:
                if tile.visible:
                    self.win.write(tile.value, bgcolor=(30, 30, 30))
                else:
                    self.win.write(' ')
            self.win.write('\n')
        if self.dungeon.player:
            for light_x, light_y in self.dungeon.get_field_of_vision(self.dungeon.player.x, self.dungeon.player.y, 5):
                if not self.dungeon[light_x, light_y].block_light:
                    self.win.settint(100, 100, 0, (light_x, light_y, 1, 1))
            self.win.putchar(PLAYER, x=self.dungeon.player.x, y=self.dungeon.player.y)


if __name__ == '__main__':
    import dungeon, player
    win = pygcurse.PygcurseWindow(40,30)
    level1 = Dungeon.load_from_file('../test/map.txt')
    level1.add_player(player.Player(1, 1))
    view = DungeonView(level1, win)
    view.draw()
    pygcurse.waitforkeypress()
