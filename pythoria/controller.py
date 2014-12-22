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
from tile import Tile

class Controller(object):
    def __init__(self, dungeon, view):
        self.dungeon = dungeon
        self.player = self.dungeon.player
        self.view = view
        self.command = None
        
    def process_event(self, event):
        "Process the events from the event loop"
        
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            global running
            running = False
        
        if self.command is not None:
            self.direction_for_command(event)
            return
            
        direction_x, direction_y = 0, 0
        if event.type == KEYDOWN and event.key == K_RIGHT:
            direction_x += 1
        elif event.type == KEYDOWN and event.key == K_LEFT:
            direction_x -= 1
        elif event.type == KEYDOWN and event.key == K_UP:
            direction_y -= 1
        elif event.type == KEYDOWN and event.key == K_DOWN:
            direction_y += 1
            
        elif event.type == KEYDOWN and event.key == K_o:
            self.command = "open"
        elif event.type == KEYDOWN and event.key == K_c:
            self.command = "close"

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
    
    def direction_for_command(self, event):
        """Get a direction from the keyboard to execute a given command in a neighbour cell."""
        if event.type == KEYDOWN and event.key == K_RIGHT:
            cell = self.dungeon[self.player.x + 1, self.player.y]
            self._execute_command(cell)
        elif event.type == KEYDOWN and event.key == K_LEFT:
            cell = self.dungeon[self.player.x - 1, self.player.y]
            self._execute_command(cell)
        elif event.type == KEYDOWN and event.key == K_UP:
            cell = self.dungeon[self.player.x, self.player.y - 1]
            self._execute_command(cell)
        elif event.type == KEYDOWN and event.key == K_DOWN:
            cell = self.dungeon[self.player.x, self.player.y + 1]
            self._execute_command(cell)
        
        
    
    def _execute_command(self, cell):
        """Execute the registered command in the given cell"""
        command = getattr(cell, self.command)
        command()
        self.command = None
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
