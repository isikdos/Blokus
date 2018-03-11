# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 14:38:56 2017

@author: Isik
"""

import clsPoint as P
import clsGameTile as GT

class GameBoard:
    """ This class represents the game board for the game Blokus.
    
    A 20 by 20 board that has tiles, each initially owned by no players.
    As the game progresses, the GameBoard's locations will be populated
    by tiles owned by players.
    
    Attributes:
        xMax: Constant. Represents the maximum X position for a game tile.
        yMax: Constant. Represents the maximum Y position for a game tile.
        xMin: Constant. Represents the minimum X position for a game tile.
        yMin: Constant. Represents the minimum Y position for a game tile.

        lsLocations: Two dimensional, 22 by 22 array of Game Tiles.
    """
    xMax = 20
    yMax = 20
    xMin = 0
    yMin = 0
    
    
    def __init__(self):
        self.lsLocations = []
        'For every row...'
        for i in range(0, self.xMax):
            self.lsLocations.append([])
            'We make a column...'
            for j in range(0, self.yMax):
                self.lsLocations[i].append(GT.GameTile(0, False))                    
   
    def PlacePiece(self, ptReference, 
                   gp, 
                   blnGhostPlacement = False,
                   blnFirstMove = False):
        """ Attempts to place a game piece onto the board.
        
        If it is detected that placing a piece would be a valid move,
        Then the tiles are put onto the game board successfully. Otherwise
        no tiles are placed at all.
        
        Arguments:
            ptReference: a tuple with an integer x and an integer y.
            gp: a GamePiece type object.
            blnFirstMove: Identifies if it is a player's first move.
        """
        if not blnGhostPlacement:
            blnValidToPlacePiece = self.ValidToPlacePiece(ptReference, 
                                                          gp,
                                                          blnFirstMove)
        else:
            blnValidToPlacePiece = True
            
        if blnValidToPlacePiece:
            PlayerTile = GT.GameTile(gp.playerID, blnGhostPlacement)
            for x, y in gp.lsLocations:
                xRef = ptReference.x + x
                yRef = ptReference.y + y   
                if (not xRef >= self.xMax and
                    not yRef >= self.yMax and
                    not xRef < self.xMin and
                    not yRef < self.xMin):
                        self.lsLocations[xRef][yRef] = PlayerTile
                
        return blnValidToPlacePiece
            
        
    def ValidToPlacePiece(self, ptReference, gp, blnFirstMove = False):
        """ Verifies if it is valid to place a piece
        
        Arguments:
            ptReference: a tuple with an integer x and an integer y.
            gp: a GamePiece type object.
            blnFirstMove: Identifies if it is a player's first move.
        """
        blnValidDiagonalPiece = False
        blnFirstMoveInCorner = False
        lsDiagonalOffsets = [(1,1),(1,-1),(-1,1),(-1,-1)]
        lsCardinalOffsets = [(0,1),(1,0),(-1,0),(0,-1)]
        lsCORNERS = [
            P.point(0,0),
            P.point(0,self.yMax - 1),
            P.point(self.xMax - 1, 0),
            P.point(self.xMax - 1, self.yMax - 1),
        ]
          
        'Can\'t use it if it\'s been used!'          
        if gp.used:
            return False
        
        'Find invalid states'
        for x, y in gp.lsLocations:
            xRef = ptReference.x + x
            yRef = ptReference.y + y
                    
            if P.point(xRef, yRef) in lsCORNERS:
                blnFirstMoveInCorner = True

            'Find if the piece is actually on the board'
            if (xRef >= self.xMax or xRef < self.xMin or \
                yRef >= self.yMax or yRef < self.yMin):
                    return False
                    
            'Find if there is a collision on this tile'
            if self.lsLocations[xRef][yRef].playerID != 0:
                return False
                
            'Find if there is a cardinally adjacent piece of the same type'
            lsEdges = []
            for w,z in lsCardinalOffsets:
                if xRef + w < self.xMax and yRef + z < self.yMax:
                    if xRef + w >= 0 and yRef + z >= 0:
                        lsEdges.append(self.lsLocations[xRef+w][yRef+z])

            for tile in lsEdges:
                if tile.playerID == gp.playerID:
                    return False
                        
            'Find if there is a diagonally adjacent piece of the same type'
            if not blnValidDiagonalPiece:
                lsCorners = []
                for w,z in lsDiagonalOffsets:
                    if xRef + w < self.xMax and yRef + z < self.yMax:
                        if xRef + w >= 0 and yRef + z >= 0:
                            lsCorners.append(self.lsLocations[xRef+w][yRef+z])

            
                for tile in lsCorners:
                    if tile.playerID == gp.playerID:
                        blnValidDiagonalPiece = True
                  
        'If we made it this far, return the valid of valid diagonal piece'
        return blnValidDiagonalPiece or (blnFirstMove and blnFirstMoveInCorner)
        
    def CheckForValidMoves(self, gamepiece, blnFirstMove):
        """ Checks to see if a piece can make any valid moves
        
        Arguments:
            gp: A game piece
            blnFirstMove: A boolean telling whether this is a first turn.
        """
        gp = gamepiece.copy()
        for x in range(self.xMin, self.xMax):
            for y in range(self.yMin, self.yMax):
                pt = P.point(x,y)
                for j in range(0,2):
                    for i in range(0,4):
                        if self.ValidToPlacePiece(pt, gp, blnFirstMove):
                            return True
                        gp.Rotate()
                    gp.Rotate()
                    gp.Flip()
                    
        return False
    
    def numPlayerTiles(self, playerID):
        """ Counts the number of tiles owned by a player
        
        Arguments:
            playerID: Integer identifying a player
        """
        points = 0
        for x in range(self.xMin, self.xMax):
            for y in range(self.yMin, self.yMax):
                if self.lsLocations[x][y].playerID == playerID:
                    points += 1
        return points
        
    def copy(self):
        """ Copies the GameBoard object """
        gb = GameBoard()
        gb.lsLocations = [[gt.copy() for gt in x] for x in self.lsLocations]
        return gb

    