#!/usr/env/ python3
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from library import get_line

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
        """
        Turn on the visibility in a radius around position (x, y)
        We first get a bounding box around our position. Then we raycast lines
        going from the position (x, y) to the bounding box. If we hit a wall,
        we make it visible and stop to look further on that ray.
        """
        border = self._get_bounding_box(x, y, radius)
        for border_x, border_y in border:
            for tile_x, tile_y in get_line(x, y, border_x, border_y):
                if self._map[tile_y][tile_x] != '#':
                    self._visibility[tile_y][tile_x] = True
                else:
                    self._visibility[tile_y][tile_x] = True
                    break
    
    def _get_bounding_box(self, x, y, radius):
        "Return the points delimiting the box at center (x,y) with size radius."
        # Need to implement circle calculation. Now make a box.
        low_x = max(0, x-radius)
        low_y = max(0, y-radius)
        high_x = min(self.width-1, x+radius)
        high_y = min(self.height-1, y+radius)
        border = [] # Perimiter of the box
        for j in range(low_y+1, high_y):
            border.append((low_x, j))
            border.append((high_x, j))
        for i in range(low_x, high_x+1):
            border.append((i, low_y))
            border.append((i, high_y))
        return border
        
    def reveal_all(self):
        "Reveal the whole map"
        self._visibility = [ [True for _ in range(self.width)] for _ in range(self.height)]
        



