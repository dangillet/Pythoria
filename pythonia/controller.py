#!/usr/env/ python
#-*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import sys
import pygcurse, pygame
from pygame.locals import *
from dungeon import Map
from dungeonview import DungeonView

class Controller(object):
    def __init__(self, dungeon, view):
        self.dungeon = dungeon
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
        old_x, old_y = self.dungeon.player.x, self.dungeon.player.y
        self.dungeon.player.x += direction_x
        self.dungeon.player.y += direction_y
        if self.dungeon.collide(self.dungeon.player):
            self.dungeon.player.x, self.dungeon.player.y = old_x, old_y

if __name__ == '__main__':
    win = pygcurse.PygcurseWindow(40, 20)
    level1 = Map.load_from_file('map/map.txt')
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
