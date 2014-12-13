#!/usr/env/ python
#-*- coding: utf-8 -*-
from __future__ import print_function

import unittest
import operator
from pythonia.pythonia import dungeon

class TestMap(unittest.TestCase):
    
    def setUp(self):
        self.test_map = dungeon.Map.load_from_file('map.txt')
    
    def test_load_from_file(self):
        
        self.assertEqual(self.test_map.width, 10)
        self.assertEqual(self.test_map.height, 4)
    
    def test_failed_loading(self):
        self.assertRaises(IOError, dungeon.Map.load_from_file, 'inexistentmap.txt')
    
    def test_getitem(self):
        self.assertEqual(self.test_map[0, 0], '#')
        self.assertEqual(self.test_map[1, 1], ' ')
        self.assertEqual(self.test_map[6, 0], '#')
        self.assertRaises(IndexError, operator.getitem, self.test_map, (10, 0))
        
if __name__ == '__main__':
    unittest.main()
