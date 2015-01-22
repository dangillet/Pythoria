#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Player():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def _set_pos(self, xy):
        """Setter for the player position. xy is a tuple with (x, y) coords."""
        x, y = xy
        self.x = x
        self.y = y
    
    pos = property(lambda self: (self.x, self.y), _set_pos, doc="""
          Position property. Reads and sets (x, y) position
          """)
