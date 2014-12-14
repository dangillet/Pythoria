#!/usr/env/ python3
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from player import Player

class Dungeon(object):
    """
    The Map object contains all the information regarding the dungeon
    """
    def __init__(self):
        self.width = self.height = None
        self._map = None
        self._visibility = None
    
    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as f:
            size = f.readline()
            dungeon = Dungeon()
            dungeon.width, dungeon.height = map(int, size.strip().split(' '))
            dungeon._map = f.readlines()
            dungeon._map = map(lambda s: s.strip(), dungeon._map)
            dungeon._visibility = [ [False for _ in range(dungeon.width)] for _ in range(dungeon.height)]
        return dungeon
    
    def add_player(self, player):
        "Add the player in the dungeon"
        self.player = player
        self.reveal(player.x, player.y, 2)
    
    def __iter__(self):
        "Iterate over the rows of the dungeon"
        for line, vis_line in zip(self._map, self._visibility):
            line = [elt if vis else ' ' for elt, vis in zip(line, vis_line)]
            yield line
    
    def __getitem__(self, key):
        "Access an element of the map with [x, y]"
        x, y = key
        if not ((0 <= x < self.width) and (0 <= y < self.height)):
            raise IndexError
        if not self._visibility[y][x]:
            return ' '
        return self._map[y][x]
    
    def collide(self, element):
        if self.__getitem__( (element.x, element.y) ) == '#':
            return True
        return False
    
    def reveal(self, x, y, radius):
        "Turn on the visibility in a radius around position (x, y)"
        # Need to implement circle calculation. Now make a box
        low_x = max(0, x-radius)
        low_y = max(0, y-radius)
        high_x = min(self.width-1, x+radius)
        high_y = min(self.height-1, y+radius)
        for j in range(low_y, high_y + 1):
            for i in range(low_x, high_x + 1):
                self._visibility[j][i] = True
    
    def reveal_all(self):
        "Reveal the whole map"
        self._visibility = [ [True for _ in range(self.width)] for _ in range(self.height)]
        



