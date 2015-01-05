#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = ['Tile', 'Door']

class Tile():
    """
    The tile contains all the information regarding its visibility, if
    it blocks line of sight, ...
    """
    
    def __init__(self, value=' ', block_light=False, blocking=False, visible=False):
        self.value = value
        self.block_light = block_light
        self.blocking = blocking
        self.visible = visible
        self.monster = None
        self.loot = []
    
    def __eq__(self, other):
        return self.value == other.value and \
               self.block_light == other.block_light and \
               self.blocking == other.blocking and \
               self.visible == other.visible
        
    def __ne__(self, other):
        return not self == other
    
    def __repr__(self):
        return '<Tile {0} {1}>'.format(self.value, 'visible' if self.visible else 'not visible')
    
    def open(self):
        """Cannot perform that action"""
        return False
    
    def close(self):
        """Cannot perform that action"""
        return False

class Door(Tile):
    """
    A Tile representing a door. It can be opened or closed.
    """
    def __init__(self, value='+', block_light=True, blocking=True, visible=False):
        super(Door, self).__init__(value, block_light, blocking, visible)
    
    def open(self):
        """If the door is closed, open it."""
        if self.value == '+':
            self.blocking = False
            self.block_light = False
            self.value = "'"
            return True
        return False
    
    def close(self):
        """If the door is opened, close it."""
        if self.value == "'":
            self.blocking = True
            self.block_light = True
            self.value = "+"
            return True
        return False
