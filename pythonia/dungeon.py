#!/usr/env/ python3
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from player import Player

class Map(object):
    def __init__(self):
        self.width = self.height = None
        self._map = None
        self.player = Player(1, 1)
    
    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as f:
            size = f.readline()
            dungeon = Map()
            dungeon.width, dungeon.height = map(int, size.strip().split(' '))
            dungeon._map = f.readlines()
            dungeon._map = map(lambda s: s.strip(), dungeon._map)
        return dungeon
    
    def __iter__(self):
        "Iterate over the rows of the dungeon"
        for line in self._map:
            yield line
    
    def __getitem__(self, key):
        "Access an element of the map with [x, y]"
        x, y = key
        if not ((0 <= x < self.width) and (0 <= y < self.height)):
            raise IndexError
        return self._map[y][x]
    
    def collide(self, element):
        if self.__getitem__( (element.x, element.y) ) == '#':
            return True
        return False


