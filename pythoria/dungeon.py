#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
import itertools, codecs
from library import get_line, get_circle

class Tile(object):
    """
    The tile contains all the information regarding its visibility, if
    it blocks line of sight, ...
    """
    
    def __init__(self, value=' ', block_light=False, blocking=False, visible=False):
        self.value = value
        self.block_light = block_light
        self.blocking = blocking
        self.visible = visible
    
    def __eq__(self, other):
        return self.value == other.value and \
               self.block_light == other.block_light and \
               self.blocking == other.blocking and \
               self.visible == other.visible
        
    def __ne__(self, other):
        return not self == other
    
    def __repr__(self):
        return '<Tile {0}{1}>'.format(self.value, ' visible' if self.visible else '')
        
class Dungeon(object):
    """
    The Dungeon object contains all the information regarding the dungeon
    """
    def __init__(self):
        self.width = self.height = None
        self._map = None
        self.player = None
    
    @classmethod
    def load_from_file(cls, filename):
        """
        Load a dungeon saved in a text file.
        Format: first line gives number of rows and columns to consider from the
        text file.
        Following lines give a text representation of the dungeon.
        Wall: #
        """
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            size = f.readline()
            dungeon = Dungeon()
            dungeon.width, dungeon.height = map(int, size.strip().split(' '))
            dungeon_map = f.readlines()
            dungeon_map = list(map(lambda s: s.strip('\n'), dungeon_map))
            dungeon._map = []
            for row_idx, row in enumerate(dungeon_map):
                row_tiles = []
                for col_idx, col in enumerate(row):
                    if col == '#':
                        row_tiles.append(Tile('#', block_light=True, blocking=True))
                    elif col == ' ':
                        row_tiles.append(Tile())
                    else:
                        raise ValueError("Character '{0}' unrecognized at row {1} col {2}".format(col, row_idx, col_idx))
                dungeon._map.append(row_tiles)
        return dungeon
    
    def add_player(self, player):
        "Add the player in the dungeon"
        self.player = player
        self.player.fov = self.get_field_of_vision(player.x, player.y, 5)
        self.reveal(self.player.fov)
    
    def __iter__(self):
        "Iterate over the rows of the dungeon"
        for line in self._map:
            yield line
    
    def __getitem__(self, key):
        "Access the Tile at position [x, y]"
        x, y = key
        if not ((0 <= x < self.width) and (0 <= y < self.height)):
            raise IndexError
        return self._map[y][x]
    
    def collide(self, x, y):
        "Check if the Tile at position (x, y) is blocking."
        if self[x, y].blocking:
            return True
        return False
    
    def reveal(self, cells):
        """
        Turn on the visibility in the given cells
        """
        for tile_x, tile_y in cells:
            self[tile_x, tile_y].visible = True
    
    def get_field_of_vision(self, x, y, radius):
        """
        Returns a list of tile coordinates in the field of vision.
        We first get a bounding circle around our position. Then we raycast lines
        going from the position (x, y) to the bounding circle. If we hit a block_light Tile,
        we make it visible and stop to look further on that ray.
        """
        points = set()
        border = self._get_bounding_circle(x, y, radius)
        for border_x, border_y in border:
            for tile_x, tile_y in get_line(x, y, border_x, border_y):
                points.add( (tile_x, tile_y) )
                if not self[tile_x, tile_y].block_light:
                    # To remove artifacts, check surrounding cells for a wall
                    points.update(self._reveal_adjacent_walls(tile_x, tile_y, x, y, radius, points))
                else:
                    break
        return points
    
    def _reveal_adjacent_walls(self, x, y, pos_x, pos_y, radius, points_visited):
        """
        In order to remove artifacts in the field of view, we show all Tiles
        adjacent to a visible non blocking-light Tile. We make sure this new tile
        remains within the given radius. If the adjacent cell is not a wall, we check
        if we have line of sight between this cell and the (pos_x, pos_y) position.
        x, y is the position of the tile from where we check the surrounding.
        pos_x, pos_y: the position from where we reveal cells, normally
        the player position.
        radius: the vision radius
        points: the set containing the points already visited
        Adapted from: https://sites.google.com/site/jicenospam/visibilitydetermination
        """

        def iter_adjacent_cells(cells):
            "Helper function to iterate over the adjacent cells in the given iterator"
            for offset_x , offset_y in cells:
                if not (abs(offset_x) or abs(offset_y)): # Skip position (0, 0)
                    continue
                if (x + offset_x, y + offset_y) in points_visited:
                    continue
                if (x + offset_x - pos_x)**2 + (y + offset_y - pos_y)**2 > (radius+0.5)**2:
                    continue
                if not self[x + offset_x, y + offset_y].block_light:
                    if not self._free_line_of_sight(pos_x, pos_y, x + offset_x, y + offset_y):
                        continue
                points.add( (x + offset_x, y + offset_y) )
        
        points = set()
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
        return points
    
    def _free_line_of_sight(self, x0, y0, x1, y1):
        "Check if the line is free of cells blocking the light."
        line = get_line(x0, y0, x1, y1)
        for cell in line:
            if self[cell].block_light:
                return False
        return True
    
    def _get_bounding_box(self, x, y, radius):
        "Return the points delimiting the box at center (x, y) with size radius."
        low_x, low_y = self._clamp_in_map(x - radius, y - radius)
        high_x, high_y = self._clamp_in_map(x + radius, y + radius)
        border = [] # Perimiter of the box
        for j in range(low_y + 1, high_y):
            border.append((low_x, j))
            border.append((high_x, j))
        for i in range(low_x, high_x + 1):
            border.append((i, low_y))
            border.append((i, high_y))
        return border
    
    def _get_bounding_circle(self, x, y, radius):
        "Return the points delimiting the circle  at center (x, y) with given radius."
        points = get_circle(x, y, radius)
        for i, point in enumerate(points):
            x, y = point
            if not ((0 <= x < self.width) and (0 <= y < self.height)):
                x, y = self._clamp_in_map(x, y)
                points[i] = (x, y)
        return points
    
    def _clamp_in_map(self, x, y):
        "Returns the position (x, y) bounded by the map geometry"
        x = min(max(0, x), self.width - 1)
        y = min(max(0, y), self.height - 1)
        return x, y
        
    def reveal_all(self):
        "Reveal the whole map"
        for row in self._map:
            for tile in row:
                tile.visible=True
        



