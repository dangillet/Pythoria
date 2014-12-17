#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def _set_pos(self, x, y):
        self.x = x
        self.y = y
    
    pos = property(lambda self: (self.x, self.y), _set_pos, doc="""
          Position property. Reads and sets (x, y) position
          """)
