# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 22:12:42 2017

@author: Isik
"""

class GameTile:
    """ Represents any given tile of the GameBoard.
    
    Attributes:
        playerID: The ID of the player to whom the tile belongs
        isGhost: A boolean that lets the program know the tile
            has actually been placed.
    """
    
    def __init__(self, playerID, isGhost = False, isReal = True):
        self.playerID = playerID
        self.isGhost = isGhost
        self.isReal = isReal
        
    def copy(self):
        gt = GameTile(self.playerID, self.isGhost, self.isReal)
        return gt