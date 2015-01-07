#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from pythoria import tile

class TestTile(unittest.TestCase):
    def test_eq(self):
        t1 = tile.Tile('#', True, True, True)
        t2 = tile.Tile('#', True, True, True)
        t3 = tile.Tile('#', True, True, False)
        self.assertTrue(t1 == t2)
        self.assertFalse(t1 == t3)
        self.assertTrue(t1 != t3)

class TestDoor(unittest.TestCase):
    def setUp(self):
        self.door = tile.Door('+')
        
    def test_init(self):
        self.assertTrue(self.door.blocking)
        self.assertTrue(self.door.block_light)
        self.assertEqual(self.door.value, '+')
    
    def test_open(self):
        self.assertTrue(self.door.open())
        self.assertFalse(self.door.blocking)
        self.assertFalse(self.door.block_light)

    def test_close(self):
        self.assertFalse(self.door.close())
        self.door.open()
        self.assertTrue(self.door.close())
        self.assertTrue(self.door.blocking)
        self.assertTrue(self.door.block_light)

if __name__ == '__main__':
    unittest.main()
