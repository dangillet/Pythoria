#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division

import unittest
import operator
from pythoria import dungeon

EMPTY_SPACE = dungeon.Tile()
WALL = dungeon.Tile('#', True, True, True)
WALL_HIDDEN = dungeon.Tile('#', True, True)

class TestTile(unittest.TestCase):
    def test_eq(self):
        t1 = dungeon.Tile('#', True, True, True)
        t2 = dungeon.Tile('#', True, True, True)
        t3 = dungeon.Tile('#', True, True, False)
        self.assertTrue(t1 == t2)
        self.assertFalse(t1 == t3)
        self.assertTrue(t1 != t3)
        
class TestDungeon(unittest.TestCase):
    
    def setUp(self):
        self.test_map = dungeon.Dungeon.load_from_file('map.txt')
    
    def test_load_from_file(self):
        self.assertEqual(self.test_map.width, 10)
        self.assertEqual(self.test_map.height, 6)
        self.assertRaises(ValueError, dungeon.Dungeon.load_from_file, 'map_wrong_char.txt')
    
    def test_failed_loading(self):
        self.assertRaises(IOError, dungeon.Dungeon.load_from_file, 'inexistentmap.txt')
    
    def test_getitem(self):
        self.assertEqual(self.test_map[0, 0], WALL_HIDDEN)
        self.assertEqual(self.test_map[1, 1], EMPTY_SPACE)
        self.assertEqual(self.test_map[6, 0], WALL_HIDDEN)
        self.assertRaises(IndexError, operator.getitem, self.test_map, (10, 0))
    
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
        
        
if __name__ == '__main__':
    unittest.main()
