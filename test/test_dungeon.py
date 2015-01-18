#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import operator
from pythoria import dungeon, tile

EMPTY_SPACE = tile.Tile()
WALL = tile.Tile('#', True, True, True)
WALL_HIDDEN = tile.Tile('#', True, True)
        
class TestDungeon(unittest.TestCase):
    
    def setUp(self):
        self.test_map = dungeon.Dungeon.load_from_file('map.txt')
    
    def test_init_empty(self):
        test_map = dungeon.Dungeon(10, 12)
        self.assertEqual(test_map.width, 10)
        self.assertEqual(test_map.height, 12)
        count = 0
        for row in test_map:
            for col in row:
                self.assertEqual(col, dungeon.Tile())
                count += 1
        self.assertEqual(count, 10 * 12)
    
    def test_init_map(self):
        the_map = ['######', '# # ##', '# # ##', '######']
        test_map = dungeon.Dungeon(6, 4, the_map)
        self.assertEqual(test_map.width, 6)
        self.assertEqual(test_map.height, 4)
        self.assertEqual(test_map[2, 1], WALL_HIDDEN)
        self.assertEqual(test_map[3, 1], EMPTY_SPACE)
        
    def test_init_map_adjust_size(self):
        the_map = ['######', '# # ##', '# # ##', '######']
        test_map = dungeon.Dungeon(7, 5, the_map)
        self.assertEqual(test_map.width, 7)
        self.assertEqual(test_map.height, 5)
        self.assertEqual(test_map[6, 0], EMPTY_SPACE)
        self.assertEqual(test_map[0, 4], EMPTY_SPACE)
    
    def test_load_from_file(self):
        self.assertEqual(self.test_map.width, 10)
        self.assertEqual(self.test_map.height, 8)
        self.assertRaises(ValueError, dungeon.Dungeon.load_from_file, 'map_wrong_char.txt')
    
    def test_iter(self):
        height = 0
        for line in self.test_map:
            self.assertEqual(len(line), self.test_map.width)
            height += 1
        self.assertEqual(height, self.test_map.height)
    
    def test_failed_loading(self):
        self.assertRaises(IOError, dungeon.Dungeon.load_from_file, 'inexistentmap.txt')
    
    def test_within_bounds(self):
        self.assertTrue(self.test_map._within_bounds(4, 6))
        self.assertFalse(self.test_map._within_bounds(11, 6))
        self.assertFalse(self.test_map._within_bounds(9, 10))
    
    def test_getitem(self):
        self.assertEqual(self.test_map[0, 0], WALL_HIDDEN)
        self.assertEqual(self.test_map[1, 1], EMPTY_SPACE)
        self.assertEqual(self.test_map[6, 0], WALL_HIDDEN)
        self.assertRaises(IndexError, operator.getitem, self.test_map, (10, 0))
    
    def test_getitem_slice(self):
        first_two_rows = self.test_map[0: 2]
        self.assertEqual(first_two_rows[0][0:2], [WALL_HIDDEN, WALL_HIDDEN])
        self.assertEqual(first_two_rows[1][0:2], [WALL_HIDDEN, EMPTY_SPACE])
    
    def test_setitem(self):
        new_tile = tile.Tile('#', True, False, True)
        self.test_map[2, 3] = new_tile
        self.assertIs(self.test_map[2, 3], new_tile)
        self.assertRaises(TypeError, operator.setitem, self.test_map, (2, 3), object())
        self.assertRaises(IndexError, operator.setitem, self.test_map, (10, 0), new_tile)
    
    def test_collide(self):
        self.assertTrue(self.test_map.collide(0, 0))
        self.assertFalse(self.test_map.collide(3, 3))
    
    def test_get_bounding_box(self):
        self.assertSetEqual(set(self.test_map._get_bounding_box(2, 2, 1)),
                                {(1,1), (2,1), (3,1),
                                 (1,2),        (3,2),
                                 (1,3), (2,3), (3,3)})
    
    def test_get_bounding_circle(self):
        self.assertSetEqual(set(self.test_map._get_bounding_circle(2, 2, 2)),
                                {(1,0), (2,0), (3,0),
                          (0,1),                      (4,1),
                          (0,2),                      (4,2),
                          (0,3),                      (4,3),
                                 (1,4), (2,4), (3,4)})
    
    def test_reveal(self):
        self.test_map.reveal([(4, 0)])

        self.assertEqual(self.test_map[4, 0], WALL)
        self.assertEqual(self.test_map[5, 0], WALL_HIDDEN)
    
    def test_get_field_of_vision(self):
        fov = self.test_map.get_field_of_vision(1, 1, 4)
        #    0123456
        #    #######
        #    #P....
        self.assertIn((5,0), fov)
        self.assertNotIn((6, 0), fov)
    
    def test_reveal_adjacent_walls(self):
        x, y = 1, 1
        points = self.test_map._reveal_adjacent_walls(3, 1, x, y, 5, set())
        self.assertEqual(points, {(3, 0), (4, 0), (3, 2), (4, 1), (4, 2)})

    def test_free_line_of_sight(self):
        self.assertTrue(self.test_map._free_line_of_sight(1, 1, 3, 2))
    
    def test_clamp_in_map(self):
        x, y = -1, -1
        self.assertEqual(self.test_map._clamp_in_map(x, y), (0, 0))
        width = self.test_map.width
        height = self.test_map.height
        x = width
        y = height
        self.assertEqual(self.test_map._clamp_in_map(x, y), (width - 1, height - 1))
    
    def test_get_neighbour_cells(self):
        x, y = 1, 1
        cells = [self.test_map[0, 1],
                 self.test_map[2, 1],
                 self.test_map[1, 0],
                 self.test_map[1, 2]]
        self.assertEqual(self.test_map.get_neighbour_cells(x, y), cells)
    
    def test_add_player(self):
        class MockPlayer():
            pass
        mock_player = MockPlayer()
        mock_player.x = 1
        mock_player.y = 1
        self.test_map.add_player(mock_player)
        self.assertIs(self.test_map.player, mock_player)
        self.assertEqual(self.test_map.player.fov, self.test_map.get_field_of_vision(1, 1, 5))
    
    def test_open_door(self):
        self.assertFalse(self.test_map.open_door(5, 4))
        
        door = self.test_map[6, 4]
        self.assertTrue(door.blocking)
        self.assertTrue(door.block_light)
        
        self.assertTrue(self.test_map.open_door(6, 4))
        self.assertFalse(self.test_map.open_door(6, 4))

        self.assertFalse(door.blocking)
        self.assertFalse(door.block_light)
        
    def test_close_door(self):
        self.assertFalse(self.test_map.open_door(5, 4))
        
        door = self.test_map[6, 4]
        door.open()
        self.assertFalse(door.blocking)
        self.assertFalse(door.block_light)
        
        self.assertTrue(self.test_map.close_door(6, 4))
        self.assertFalse(self.test_map.close_door(6, 4))

        self.assertTrue(door.blocking)
        self.assertTrue(door.block_light)
        
if __name__ == '__main__':
    unittest.main()
