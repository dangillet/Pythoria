#!/usr/env/ python
#-*- coding: utf-8 -*-
from __future__ import print_function

import unittest
import operator
from pythonia.pythonia import dungeon

class TestDungeon(unittest.TestCase):
    
    def setUp(self):
        self.test_map = dungeon.Dungeon.load_from_file('map.txt')
    
    def test_load_from_file(self):
        self.assertEqual(self.test_map.width, 10)
        self.assertEqual(self.test_map.height, 4)
    
    def test_failed_loading(self):
        self.assertRaises(IOError, dungeon.Dungeon.load_from_file, 'inexistentmap.txt')
    
    def test_getitem(self):
        self.test_map.reveal_all()
        self.assertEqual(self.test_map[0, 0], '#')
        self.assertEqual(self.test_map[1, 1], ' ')
        self.assertEqual(self.test_map[6, 0], '#')
        self.assertRaises(IndexError, operator.getitem, self.test_map, (10, 0))
    
    def test_get_bounding_box(self):
        self.assertEqual(set(self.test_map._get_bounding_box(2, 2, 1)),
                            set([(1,1), (2,1), (3,1),
                                 (1,2),        (3,2),
                                 (1,3), (2,3), (3,3)]))
    
    def test_reveal(self):
        self.test_map.reveal(1, 1, 1)
        self.assertEqual(self.test_map[0, 0], '#')
        self.assertEqual(self.test_map[0, 3], ' ')
        
if __name__ == '__main__':
    unittest.main()
