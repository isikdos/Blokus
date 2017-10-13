# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 00:43:45 2016

@author: Isik
"""


class GamePiece:
    used = False
    
    def __init__(self, lsLocations, playerID):
        'lsLocations defines the positions of all blocks of the piece'
        'Reference (0,0) is at the bottom left of the grid'
        self.lsLocations = lsLocations
        self.playerID = playerID
        
    '''
    Rotates lsLocations 90 degress clockwise
    '''    
    def Rotate(self):
        self.lsLocations = [(-y,x) for x,y in self.lsLocations]
    
    '''
    Flips the  piece around the Y=0 axis
    '''
    def Flip(self):
        self.lsLocations = [(-x,y) for x,y in self.lsLocations]
        
    '''
    Creates unreferenced copy to itself
    '''
    def copy(self):
        gp = GamePiece(self.lsLocations[:], self.playerID)
        gp.used = self.used
        return gp
        