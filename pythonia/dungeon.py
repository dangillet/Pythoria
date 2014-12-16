#!/usr/env/ python3
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import itertools
from library import get_line, get_circle

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
        self.reveal(player.x, player.y, 5)
    
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
        
        return self._map[y][x]
    
    def show_at(self, x, y):
        """
        Returns the element of the map at position (x, y)
        taking into consideration the visibility.
        """
        item = self.__getitem__( (x, y) )
        if not self._visibility[y][x]:
            return ' '
        return item
    
    def collide(self, element):
        if self.__getitem__( (element.x, element.y) ) == '#':
            return True
        return False
    
    def reveal(self, x, y, radius):
        """
        Turn on the visibility in a radius around position (x, y)
        We first get a bounding circle around our position. Then we raycast lines
        going from the position (x, y) to the bounding circle. If we hit a wall,
        we make it visible and stop to look further on that ray.
        """
        border = self._get_bounding_circle(x, y, radius)
        for border_x, border_y in border:
            for tile_x, tile_y in get_line(x, y, border_x, border_y):
                if self._map[tile_y][tile_x] != '#':
                    self._visibility[tile_y][tile_x] = True
                    # To remove artifacts, check surrounding cells for a wall
                    self._reveal_adjacent_walls(tile_x, tile_y, x, y)
                else:
                    self._visibility[tile_y][tile_x] = True
                    break
    
    def _reveal_adjacent_walls(self, x, y, pos_x, pos_y):
        """
        In order to remove artifacts in the field of view, we show all walls
        adjacent to a visible empty cell.
        pos_x, pos_y is the position from where we reveal cells, normally
        the player position
        See: https://sites.google.com/site/jicenospam/visibilitydetermination
        """

        def iter_adjacent_cells(cells):
            "Helper function to iterate over the adjacent cells in the given iterator"
            for offset_x , offset_y in cells:
                if offset_x or offset_y: # Skip position (0, 0)
                    if self._map[y + offset_y][x + offset_x] == '#':
                        self._visibility[y + offset_y][x + offset_x] = True
        
        if x < pos_x:
            # NW sector
            if y < pos_y:
                iter_adjacent_cells(itertools.product((-1, 0), (-1, 0)))
            # SW
            elif y > pos_y:
                iter_adjacent_cells(itertools.product((-1, 0), (1, 0)))
            # W
            else:
                iter_adjacent_cells(itertools.product((-1, 0), (-1, 0, 1)))
        elif x > pos_x:
            # NE sector
            if y < pos_y:
                iter_adjacent_cells(itertools.product((1, 0), (-1, 0)))
            # SE
            elif y > pos_y:
                iter_adjacent_cells(itertools.product((1, 0), (1, 0)))
            # E
            else:
                iter_adjacent_cells(itertools.product((1, 0), (-1, 0, 1)))
        else:
            # N sector
            if y < pos_y:
                iter_adjacent_cells(itertools.product((-1, 0, 1), (-1, 0)))
            # S
            elif y > pos_y:
                iter_adjacent_cells(itertools.product((-1, 0, 1), (1, 0)))
    
    def _get_bounding_box(self, x, y, radius):
        "Return the points delimiting the box at center (x, y) with size radius."
        # Need to implement circle calculation. Now make a box.
        low_x = max(0, x-radius)
        low_y = max(0, y-radius)
        high_x = min(self.width-1, x+radius)
        high_y = min(self.height-1, y+radius)
        border = set() # Perimiter of the box
        for j in range(low_y+1, high_y):
            border.add((low_x, j))
            border.add((high_x, j))
        for i in range(low_x, high_x+1):
            border.add((i, low_y))
            border.add((i, high_y))
        return border
    
    def _get_bounding_circle(self, x, y, radius):
        "Return the points delimiting the circle  at center (x, y) with given radius."
        points = get_circle(x, y, radius)
        for i, point in enumerate(points):
            x, y = point
            if not ((0 <= x < self.width) and (0 <= y < self.height)):
                x = min(max(0, x), self.width - 1)
                y = min(max(0, y), self.height - 1)
                points[i] = (x, y)
        return points
        
    def reveal_all(self):
        "Reveal the whole map"
        self._visibility = [ [True for _ in range(self.width)] for _ in range(self.height)]
        


