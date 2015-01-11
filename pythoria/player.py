#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def _set_pos(self, x, y):
        self.x = x
        self.y = y
    
    pos = property(lambda self: (self.x, self.y), _set_pos, doc="""
          Position property. Reads and sets (x, y) position
          """)