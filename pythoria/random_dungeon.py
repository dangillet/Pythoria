#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random, operator
from pythoria import tile

class Room:
    """This is just a rectangle"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cx = x + width // 2
        self.cy = y + height // 2
    
    def collide(self, other):
        return not(self.x > other.x + other.width or other.x > self.x + self.width or \
                self.y > other.y + other.height or other.y > self.y + self.height)

class DungeonGenerator:
    """
    Helper class which generates a random dungeon
    
    Algorithm for the dungeon generation:
    - Place rooms_amount numbers of rooms randomly. For the moment the width and height
      are constrained between 3 and 8.
    - Create the corridors. Iterate over each room  and take the next one in the list.
      When considering the last room, we take the first room as a pair.
      Take a random spot in each pair of rooms and draw a corridor by moving first 
      horizontally and then vertically.
    - Consider the start and enf od corridor. Try to place doors if it makes sense.
      If that space is surrounded by exactly 2 walls, place a door. If it's next
      to another door, then erase this door and place a wall instead.
    - Check for lonely doors. Some doors are surrounded by 3 empty spaces. Erase
      those doors.
    """
    def generate_dungeon(self, max_width, max_height, rooms_amount):
        self.dungeon = [[tile.Tile('#', block_light=True, blocking=True) for _ in range(max_width)] for _ in range(max_height)]
        self.rooms = []
        self.corridors = []
        self.max_width = max_width
        self.max_height = max_height
        self.rooms_amount = rooms_amount

        self.create_rooms()

        self.create_corridors()
        self.check_for_lonely_doors()
    
    def place_player(self):
        room = random.choice(self.rooms)
        x = random.randint(room.x, room.x + room.width -1)
        y = random.randint(room.y, room.y + room.height -1)
        return x, y

    def show_map(self):
        print('   ', end='')
        print(''.join('{0:^3}'.format(i) for i in range(self.max_width)))
        for i, line in enumerate(self.dungeon):
            print('{0:^3}'.format(i), end='')
            print(''.join('{0:^3}'.format(_tile.value) for _tile in line))
            
    def create_rooms(self):
        min_room_size, max_room_size = 3, 8
        for _ in range(self.rooms_amount):
            while True:
                width, height = random.randint(min_room_size, max_room_size), random.randint(min_room_size, max_room_size)
                x, y = random.randint(1, self.max_width - width - 1), random.randint(1, self.max_height - height - 1)
                room = Room(x, y, width, height)
                if all(not other_room.collide(room) for other_room in self.rooms):
                    break
            self.rooms.append(room)
        
        # Fill empty tile where the rooms are
        for room in self.rooms:
            for line in self.dungeon[room.y:room.y + room.height]:
                room_tile = tile.Tile()
                line[room.x:room.x + room.width] = [room_tile for _ in range(room.width)]

    def find_closest(self):
        dist_list = []
        for other_room in self.rooms:
            if other_room is room:
                continue
            dist = (room.cx - other_room.cx)**2 + (room.cy - other_room.cy)**2
            dist_list.append( (dist, other_room) )
        
        return min(dist_list, key = operator.itemgetter(0))[1]
    
    def has_two_opposite_adjacent_walls(self, x, y):
        WALL = tile.Tile('#', True, True)
        if self.dungeon[y][x-1] == WALL and self.dungeon[y][x+1] == WALL:
            return True
        if self.dungeon[y-1][x] == WALL and self.dungeon[y+1][x] == WALL:
            return True
        return False
    
    def has_one_wall_and_one_door_opposite(self, x, y):
        DOOR = tile.Door()
        WALL = tile.Tile('#', True, True)
        if self.dungeon[y][x-1] in [WALL, DOOR] and \
            self.dungeon[y][x+1] in [WALL, DOOR] and \
            self.dungeon[y][x-1] != self.dungeon[y][x+1]:
            return True
        if self.dungeon[y-1][x] in [WALL, DOOR] and \
            self.dungeon[y+1][x] in [WALL, DOOR] and \
            self.dungeon[y-1][x] != self.dungeon[y+1][x]:
            return True
        return False
        
    def create_corridors(self):
        for i, room in enumerate(self.rooms):
            other_room = self.rooms[i+1] if i < len(self.rooms)-1 else self.rooms[0]
            x_from = random.randint(room.x, room.x + room.width -1)
            y_from = random.randint(room.y, room.y + room.height -1)
            x_to = random.randint(other_room.x, other_room.x + other_room.width -1)
            y_to = random.randint(other_room.y, other_room.y + other_room.height -1)
            
            corridor = []
            start_corridor = False
            while x_from != x_to or y_from != y_to:
                if x_from > x_to:
                    x_from -= 1
                elif x_from < x_to:
                    x_from += 1
                elif y_from > y_to:
                    y_from -= 1
                elif y_from < y_to:
                    y_from += 1
                
                if self.dungeon[y_from][x_from] == tile.Tile('#', block_light=True, blocking=True):
                    start_corridor = True
                    corridor.append( (x_from, y_from) )
                elif start_corridor and self.dungeon[y_from][x_from] == tile.Tile():
                    break
            
            self.corridors.append(corridor)
        
            # Place empty tiles for the corridor
            for x, y in corridor:
                self.dungeon[y][x] = tile.Tile()
            
            # Consider placing doors
            for x, y in (corridor[0], corridor[-1]):
                if self.has_two_opposite_adjacent_walls(x, y):
                    self.dungeon[y][x] = tile.Door()
                elif self.has_one_wall_and_one_door_opposite(x, y):
                    self.dungeon[y][x] = tile.Tile('#', True, True)

    def check_for_lonely_doors(self):
        EMPTY_SPACE = tile.Tile()
        DOOR = tile.Door()
        for y, line in enumerate(self.dungeon):
            for x, _tile in enumerate(line):
                if _tile == tile.Door():
                    count_empty_space = 0
                    # Check S  W  N  E
                    for off_x, off_y in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                        if self.dungeon[y+off_y][x+off_x] == EMPTY_SPACE:
                            count_empty_space += 1
                        elif self.dungeon[y+off_y][x+off_x] == DOOR:
                            self.dungeon[y][x] = tile.Tile()
                            break

                    if count_empty_space > 2:
                        self.dungeon[y][x] = tile.Tile()
                        
