#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division

def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points

def get_circle(x0, y0, radius):
    """
    Algorithm adapted from http://en.wikipedia.org/wiki/Midpoint_circle_algorithm
    """
    x = radius
    y = 0
    radius_error = 1 - x
    points = []
    while x >= y:
        points.append((x + x0, y + y0))
        points.append((y + x0, x + y0))
        points.append((-x + x0, y + y0))
        points.append((-y + x0, x + y0))
        points.append((-x + x0, -y + y0))
        points.append((-y + x0, -x + y0))
        points.append((x + x0, -y + y0))
        points.append((y + x0, -x + y0))
        y += 1
        if radius_error < 0:
            radius_error += 2 * y + 1
        else:
            x -= 1
            radius_error += 2 * (y - x + 1)
    return points

if __name__ == '__main__':
    import pygcurse, pygame
    win = pygcurse.PygcurseWindow(40,30)
    win.font = pygame.font.Font(None, 22)
    points = get_circle(5, 5, 5)
    for p in points:
        win.putchar('O', x=p[0], y=p[1])
    pygcurse.waitforkeypress()
            
            
    
    
    
