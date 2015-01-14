#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygcurse, pygame
from pythoria.dungeon import Dungeon

pygame.font.init()

PLAYER = '\N{WHITE SMILING FACE}' # Unicode for a smile


class DungeonView(pygcurse.PygcurseSurface):
    font = pygame.font.Font(pygame.font.match_font('consolas'), 18)

    def __init__(self, dungeon):
        self.dungeon = dungeon
        super(DungeonView, self).__init__(66, 30, DungeonView.font)
        self.autoupdate = False
        
    def draw(self):
        "Draw the dungeon and the player."
        self.setscreencolors()
        self.cursor = (0, 0)
        for line in self.dungeon:
            for tile in line:
                if tile.visible:
                    self.write(tile.value, bgcolor=(30, 30, 30))
                else:
                    self.write(' ')
            self.write('\n')
        if self.dungeon.player:
            for light_x, light_y in self.dungeon.player.fov:
                if not self.dungeon[light_x, light_y].block_light:
                    self.settint(30, 30, 0, (light_x, light_y, 1, 1))
            self.putchar(PLAYER, x=self.dungeon.player.x, y=self.dungeon.player.y)
        
        self.update()


if __name__ == '__main__':
    import dungeon, player
    win = pygcurse.PygcurseWindow(40,30)
    level1 = Dungeon.load_from_file('../test/map.txt')
    level1.add_player(player.Player(1, 1))
    view = DungeonView(level1)
    view.draw()
    view.blitto(win.surface)
    win.blittowindow()
    
    pygcurse.waitforkeypress()
