# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 19:52:27 2017

@author: Isik
"""

class point:
    """ A simple class that represents an integer point.
    
    Attributes:
        x: x coordinate
        y: y coordinate
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False