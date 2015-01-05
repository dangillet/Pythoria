#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygcurse, pygame
from pygame.locals import *

from pythoria.dungeon import Dungeon
from pythoria.dungeonview import DungeonView
from pythoria.player import Player
from pythoria.tile import Tile

class DirectionForCommand():
    def __init__(self, controller, command):
        self.controller = controller
        self.dungeon = self.controller.dungeon
        self.player = self.dungeon.player
        self.command = command
    
    def process_event(self, event):
        "Process the events from the event loop"

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.controller.event_handler.pop()
            
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            self._execute_command(1, 0)
        elif event.type == KEYDOWN and event.key == K_LEFT:
            self._execute_command(-1, 0)
        elif event.type == KEYDOWN and event.key == K_UP:
            self._execute_command(0, -1)
        elif event.type == KEYDOWN and event.key == K_DOWN:
            self._execute_command(0, 1)
    
    def _execute_command(self, dir_x, dir_y):
        """Execute the registered command in the given direction"""
        command = getattr(self.dungeon, self.command)
        command(self.player.x + dir_x, self.player.y + dir_y)
        self.player.fov = self.dungeon.get_field_of_vision(self.player.x,
                                                           self.player.y,
                                                           5)
        self.dungeon.reveal(self.player.fov)
        self.controller.event_handler.pop()

class GameEventHandler():
    def __init__(self, controller):
        self.controller = controller
        self.dungeon = self.controller.dungeon
    
    def process_event(self, event):
        "Process the events from the event loop"

        if event.type == KEYDOWN and event.key == K_RIGHT:
            self.dungeon.move_player(1, 0)
        elif event.type == KEYDOWN and event.key == K_LEFT:
            self.dungeon.move_player(-1, 0)
        elif event.type == KEYDOWN and event.key == K_UP:
            self.dungeon.move_player(0, -1)
        elif event.type == KEYDOWN and event.key == K_DOWN:
            self.dungeon.move_player(0, 1)
        elif event.type == KEYDOWN and event.key == K_o:
            self.controller.event_handler.append(DirectionForCommand(self.controller, "open_door"))
        elif event.type == KEYDOWN and event.key == K_c:
            self.controller.event_handler.append(DirectionForCommand(self.controller, "close_door"))

class Controller():
    def __init__(self, dungeon, view):
        self.dungeon = dungeon
        self.player = self.dungeon.player
        self.view = view
        self.event_handler = [GameEventHandler(self)]
        
    def process_event(self, event):
        "Process the events from the event loop"
        
        if event.type == QUIT:
            global running
            running = False
        
        self.event_handler[-1].process_event(event)
        
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
