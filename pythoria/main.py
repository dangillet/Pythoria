#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygcurse, pygame
from pygame.locals import *

from dungeon import Dungeon
from player import Player
from messagebox import MessageBox
from gameview import GameView
from dungeonview import ScrollingView
from hudview import HUDView
from messageboxview import MessageBoxView
from controller import Controller

def main():
    """
    Quick game setup for testing purposes.
    """
    win = pygcurse.PygcurseWindow(80, 30)
    win.font = pygame.font.Font(pygame.font.match_font('consolas'), 18)
    level1 = Dungeon.load_from_file('map/bigmap.txt')
    player = Player(1, 1)
    level1.add_player(player)
    msgbox = MessageBox()

    view = GameView(
        win,
        {
            ScrollingView(level1):         (0  ,   0),
            HUDView(player):               (700,   0),
            MessageBoxView(msgbox, 80, 5): (0  , 460)
        }
    )

    controller = Controller(level1, msgbox,  view)
    win.autoupdate = False
    mainClock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                controller.process_event(event)

        controller.view.draw()
        win.blittowindow()
        mainClock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
