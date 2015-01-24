#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random, operator
from pythoria import tile

#random.seed(14)

class Room:
    """
    This is a rectangle defined by its top left corner, a width and height.
    """
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
    
    def __repr__(self):
        return "<Room {0} {1} {2} {3}>".format(self.x, self.y, self.width, self.height)

class Corridor:
    def __init__(self, room_one, room_two):
        self.room_one = room_one
        self.room_two = room_two
    
    def __eq__(self, other):
        return (self.room_one == other.room_one and self.room_two == other.room_two) or \
               (self.room_one == other.room_two and self.room_two == other.room_one)
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self.room_one) ^ hash(self.room_two)
    
    def __repr__(self):
        return "({0}--{1})".format(self.room_one, self.room_two)
    
class DungeonGenerator:
    """
    Helper class which generates a random dungeon
    
    Algorithm for the dungeon generation:
    - Place rooms_amount numbers of rooms randomly. For the moment the width and height
      are constrained between 3 and 8.
    - Construct a graph of rooms and edges being the corridors connecting rooms close
      to each other.
    - Create the corridors. Iterate over each room  and take the edge to connect to the
      next room.
      Take a random spot in each pair of rooms and draw a corridor by moving first 
      horizontally and then vertically.
    - Consider the start and enf of corridor. Try to place doors if it makes sense.
      If that space is surrounded by exactly 2 walls, place a door. If it's next
      to another door, then erase this door and place a wall instead.
    - Check for lonely doors. Some doors are surrounded by 3 empty spaces. Erase
      those doors.
    """
    def generate_dungeon(self, max_width, max_height, rooms_amount):
        self.dungeon = [[tile.Tile('#', block_light=True, blocking=True) for _ in range(max_width)] for _ in range(max_height)]
        self.rooms = []
        self.corridors = set()
        self.max_width = max_width
        self.max_height = max_height
        self.rooms_amount = rooms_amount

        self.create_rooms() # Maybe move them apart.
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
        min_room_size, max_room_size = 3, 7
        for _ in range(self.rooms_amount):
            counter = 0
            while True:
                width, height = random.randint(min_room_size, max_room_size), random.randint(min_room_size, max_room_size)
                x, y = random.randint(1, self.max_width - width - 1), random.randint(1, self.max_height - height - 1)
                room = Room(x, y, width, height)
                if all(not other_room.collide(room) for other_room in self.rooms):
                    break
                counter += 1
                if counter > 1000:
                    raise RuntimeError("Trying to place a random room but failed to find an empty space after {0} attempts".format(counter))
            self.rooms.append(room)
            self.move_rooms_apart()
        
        
        self.move_rooms_apart()
        # Fill empty tile where the rooms are
        for room in self.rooms:
            for line in self.dungeon[room.y:room.y + room.height]:
                room_tile = tile.Tile()
                line[room.x:room.x + room.width] = [room_tile for _ in range(room.width)]

    def room_collides_with_others(self, room):
        for other_room in self.rooms:
            if other_room is room:
                continue
            if other_room.collide(room):
                return True
        return False
    
    def move_rooms_apart(self):
        cx = self.max_width // 2
        cy = self.max_height // 2
        for room in self.rooms:
            if room.x - cx <= 0 and room.y - cy <= 0:
                offset_x = -1
                offset_y = -1
            elif room.x - cx <= 0 and room.y - cy > 0:
                offset_x = -1
                offset_y = 1
            elif room.x - cx > 0 and room.y - cy <= 0:
                offset_x = 1
                offset_y = -1
            elif room.x - cx > 0 and room.y - cy > 0:
                offset_x = 1
                offset_y = 1
                
            room.x += offset_x
            room.y += offset_y
            self.constrain_room_in_dungeon(room)
            if self.room_collides_with_others(room):
                room.x -= offset_x
                room.y -= offset_y
        
    def constrain_room_in_dungeon(self, room):
        room.x = min(max(room.x, 1), self.max_width - room.width - 1)
        room.y = min(max(room.y, 1), self.max_height - room.height - 1)
    
    def find_closest(self, room, rooms):
        dist_list = []
        for other_room in rooms:
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
    
    def find_corridor(self, x_from, y_from, x_to, y_to):
        squares = []
        while x_from != x_to or y_from != y_to:
            if x_from > x_to:
                x_from -= 1
            elif x_from < x_to:
                x_from += 1
            elif y_from > y_to:
                y_from -= 1
            elif y_from < y_to:
                y_from += 1
            squares.append( (x_from, y_from) )
        
        start = end = None
        for idx, (x, y) in enumerate(squares):
            if self.dungeon[y][x] == tile.Tile('#', block_light=True, blocking=True):
                start = idx
                break
        for idx, (x, y) in enumerate(reversed(squares)):
            if self.dungeon[y][x] == tile.Tile('#', block_light=True, blocking=True):
                end = -idx
                break

        return squares[start:end]
        
    def create_corridors(self):
        visited = set()
        not_visited = set(self.rooms)
        room = not_visited.pop()
        while not_visited:
            other_room = self.find_closest(room, not_visited)
            self.corridors.add(Corridor(room, other_room))
            not_visited.remove(other_room)
            room = other_room
        
        for corridor in self.corridors:
            room = corridor.room_one
            other_room = corridor.room_two
            x_from = random.randint(room.x, room.x + room.width -1)
            y_from = random.randint(room.y, room.y + room.height -1)
            x_to = random.randint(other_room.x, other_room.x + other_room.width -1)
            y_to = random.randint(other_room.y, other_room.y + other_room.height -1)

            corridor_squares = self.find_corridor(x_from, y_from, x_to, y_to)
        
            # Place empty tiles for the corridor
            for x, y in corridor_squares:
                self.dungeon[y][x] = tile.Tile()
            
            # Consider placing doors
            for x, y in (corridor_squares[0], corridor_squares[-1]):
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
                        
if __name__ == '__main__':
    dg = DungeonGenerator()
    dg.generate_dungeon(25, 20, 7)
    dg.show_map()
