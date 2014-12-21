#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division

import sys
import pygcurse, pygame
from pygame.locals import *
import dungeon
from dungeon import Dungeon
from dungeonview import DungeonView
from player import Player

class Controller(object):
    def __init__(self, dungeon, view):
        self.dungeon = dungeon
        self.player = self.dungeon.player
        self.view = view
        
    def process_event(self, event):
        "Process the events from the event loop"
        direction_x, direction_y = 0, 0
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            global running
            running = False
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            direction_x += 1
        elif event.type == KEYDOWN and event.key == K_LEFT:
            direction_x -= 1
        elif event.type == KEYDOWN and event.key == K_UP:
            direction_y -= 1
        elif event.type == KEYDOWN and event.key == K_DOWN:
            direction_y += 1
        elif event.type == KEYDOWN and event.key == K_o:
            neighbour_cells = self.dungeon.get_neighbour_cells(*self.player.pos)
            for cell in neighbour_cells:
                if cell.open():
                    self.player.fov = self.dungeon.get_field_of_vision(self.player.x,
                                                               self.player.y,
                                                               5)
                    self.dungeon.reveal(self.player.fov)
                    break
        elif event.type == KEYDOWN and event.key == K_c:
            neighbour_cells = self.dungeon.get_neighbour_cells(*self.player.pos)
            for cell in neighbour_cells:
                if cell.close():
                    self.player.fov = self.dungeon.get_field_of_vision(self.player.x,
                                                               self.player.y,
                                                               5)
                    break

        if direction_x or direction_y:
            old_x, old_y = self.player.x, self.player.y
            self.player.x += direction_x
            self.player.y += direction_y
            if self.dungeon.collide(*self.player.pos):
                self.player.x, self.player.y = old_x, old_y
            else:
                self.player.fov = self.dungeon.get_field_of_vision(self.player.x,
                                                               self.player.y,
                                                               5)
            self.dungeon.reveal(self.player.fov)

if __name__ == '__main__':
    win = pygcurse.PygcurseWindow(40, 20)
    level1 = Dungeon.load_from_file('map/map.txt')
    level1.add_player(Player(1, 1))
    view = DungeonView(level1, win)
    controller = Controller(level1, view)
    win.autoupdate = False
    mainClock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            controller.process_event(event)
        
        win.setscreencolors()
        win.cursor = (0,0)
        view.draw()
        win.update()
        mainClock.tick(30)

    pygame.quit()
    sys.exit()
