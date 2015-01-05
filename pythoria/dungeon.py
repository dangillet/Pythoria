#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
from pythoria.library import get_line, get_circle
from pythoria.tile import *

        
class Dungeon():
    """
    The Dungeon object contains all the information regarding the dungeon
    """
    def __init__(self, width=None, height=None, dungeon_map=None):
        self.width = width
        self.height = height
        self._map = None
        self.player = None
        
        if dungeon_map:
            self._parse_text(dungeon_map)
        elif width is not None and height is not None:
            self._map = [[Tile() for col in range(width)] for row in range(height)]
            
    def _parse_text(self, dungeon_map):
        """
        Parse a list of strings into a Dungeon Map filled with Tiles
        Whitespace for empty tile
        # for walls
        """
        for idx, line in enumerate(dungeon_map):
            if len(line) < self.width:
                dungeon_map[idx] += ' ' * (self.width - len(line))
        if len(dungeon_map) < self.height:
            dungeon_map.extend([' ' * self.width for _ in range(self.height - len(dungeon_map))])
        
        self._map = []
        for row_idx, row in enumerate(dungeon_map):
            row_tiles = []
            for col_idx, col in enumerate(row):
                if col == '#':
                    row_tiles.append(Tile('#', block_light=True, blocking=True))
                elif col == ' ':
                    row_tiles.append(Tile())
                elif col == '+':
                    row_tiles.append(Door('+'))
                elif col == "'":
                    row_tiles.append(Door("'"))
                else:
                    raise ValueError("Character '{0}' unrecognized at row {1} col {2}".format(col, row_idx, col_idx))
            self._map.append(row_tiles)
            
    @classmethod
    def load_from_file(cls, filename):
        """
        Load a dungeon saved in a text file.
        Format: first line gives number of rows and columns to consider from the
        text file.
        Following lines give a text representation of the dungeon.
        If given width or height is greater than actual text, white spaces added
        to fulfill width and height criteria.
        Wall: #
        """
        with open(filename, 'r', encoding='utf-8') as f:
            size = f.readline()
            width, height = map(int, size.strip().split(' '))
            dungeon_map = f.readlines()
            dungeon_map = list(map(lambda s: s.strip('\r\n'), dungeon_map))
        
        return cls(width, height, dungeon_map)
    
    def add_player(self, player):
        "Add the player in the dungeon"
        self.player = player
        self.player.fov = self.get_field_of_vision(player.x, player.y, 5)
        self.reveal(self.player.fov)
    
    def move_player(self, dir_x, dir_y):
        """Move the player in the given direction"""
        old_x, old_y = self.player.x, self.player.y
        self.player.x += dir_x
        self.player.y += dir_y
        if self.collide(*self.player.pos):
            self.player.x, self.player.y = old_x, old_y
        else:
            self.player.fov = self.get_field_of_vision(self.player.x,
                                                       self.player.y,
                                                       5)
            self.reveal(self.player.fov)
    
    def __iter__(self):
        "Iterate over the rows of the dungeon"
        for line in self._map:
            yield line
    
    def _within_bounds(self, x, y):
        """Check if indices (x, y) are within the map bounds."""
        return (0 <= x < self.width) and (0 <= y < self.height)
    
    def __getitem__(self, key):
        "Access the Tile at position [x, y]"
        x, y = key
        if not self._within_bounds(x, y):
            raise IndexError
        return self._map[y][x]
    
    def __setitem__(self, key, tile):
        "Set the Tile at position [x, y]"
        x, y = key
        if not self._within_bounds(x, y):
            raise IndexError
        if not isinstance(tile, Tile):
            raise TypeError("Tried to assign an object of type {0}. Expecting type Tile". format(type(tile)))
        self._map[y][x] = tile
    
    def collide(self, x, y):
        "Check if the Tile at position (x, y) is blocking."
        return self[x, y].blocking
    
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
            if not self._within_bounds(x, y):
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
        for row in self:
            for tile in row:
                tile.visible=True
        
    def get_neighbour_cells(self, x, y):
        """Returns the cells adjacent to the position (x, y)"""
        return [self[x + i, y] for i in (-1, 1)] +  [self[x, y + j] for j in (-1, 1)]
    
    def open_door(self, x, y):
        """
        Open a Door Tile at position x, y
        Return True if this operation is succefull. False otherwise.
        """
        cell = self[x, y]
        return cell.open()
    
    def close_door(self, x, y):
        """
        Close a Door Tile at position x, y
        Return True if this operation is succefull. False otherwise.
        """
        cell = self[x, y]
        return cell.close()


