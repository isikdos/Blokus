# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 14:38:56 2017

@author: Isik
"""

import clsPoint as P
import clsGameTile as GT

PLAYER1TILE = GT.GameTile(1, False)
PLAYER2TILE = GT.GameTile(2, False)
PLAYER3TILE = GT.GameTile(3, False)
PLAYER4TILE = GT.GameTile(4, False)

fakePLAYER1TILE = GT.GameTile(1, True, False)
fakePLAYER2TILE = GT.GameTile(2, True, False)
fakePLAYER3TILE = GT.GameTile(3, True, False)
fakePLAYER4TILE = GT.GameTile(4, True, False)

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
        xBound: A constant that represents the behind-the-scenes size of 
            the GameBoard
        yBound: A constant that represents the behind-the-scenes size of
            the GameBoard
        lsLocations: Two dimensional, 22 by 22 array of Game Tiles.
    """
    xMax = 21
    yMax = 21
    xMin = 1
    yMin = 1
    
    xBound = 22
    yBound = 22
    
    
    def __init__(self):
        self.lsLocations = []
        'For every row...'
        for i in range(0, self.xBound):
            self.lsLocations.append([])
            'We make a column...'
            for j in range(0, self.yBound):
                self.lsLocations[i].append(GT.GameTile(0, False))                    
        
        'And we defined dummy-pieces so that players can start in the'
        'correct places.'
        self.lsLocations[0][0]                              = PLAYER1TILE
        self.lsLocations[self.xBound - 1][self.yBound - 1]  = PLAYER2TILE
        self.lsLocations[0][self.xBound - 1]                = PLAYER3TILE
        self.lsLocations[self.yBound - 1][0]                = PLAYER4TILE
        
        self.lsLocations[1][1]                              = fakePLAYER1TILE
        self.lsLocations[self.xBound - 2][self.yBound - 2]  = fakePLAYER2TILE
        self.lsLocations[1][self.xBound - 2]                = fakePLAYER3TILE
        self.lsLocations[self.yBound - 2][1]                = fakePLAYER4TILE
   
    def PlacePiece(self, ptReference, gp, blnGhostPlacement = False):
        """ Attempts to place a game piece onto the board.
        
        If it is detected that placing a piece would be a valid move,
        Then the tiles are put onto the game board successfully. Otherwise
        no tiles are placed at all.
        
        Arguments:
            ptReference: a tuple with an integer x and an integer y.
            gp: a GamePiece type object.
        """
        if not blnGhostPlacement:
            blnValidToPlacePiece = self.ValidToPlacePiece(ptReference, gp)
        else:
            blnValidToPlacePiece = True
            
        if blnValidToPlacePiece:
            PlayerTile = GT.GameTile(gp.playerID, blnGhostPlacement)
            for x, y in gp.lsLocations:
                xRef = ptReference.x + x
                yRef = ptReference.y + y      
                if xRef >= self.xMax:
                    xRef = self.xMax - 1
                if yRef >= self.xMax:
                    yRef = self.xMax - 1
                self.lsLocations[xRef][yRef] = PlayerTile
                
        return blnValidToPlacePiece
            
        
    def ValidToPlacePiece(self, ptReference, gp):
        """ Verifies if it is valid to place a piece
        
        Arguments:
            ptReference: a tuple with an integer x and an integer y.
            gp: a GamePiece type object.
        """
        blnValidDiagonalPiece = False
        lsDiagonalOffsets = [(1,1),(1,-1),(-1,1),(-1,-1)]
        lsCardinalOffsets = [(0,1),(1,0),(-1,0),(0,-1)]
          
        'Can\'t use it if it\'s been used!'          
        if gp.used:
            return False
            
        'Find invalid states'
        for x, y in gp.lsLocations:
            xRef = ptReference.x + x
            yRef = ptReference.y + y

            'Find if the piece is actually on the board'
            if (xRef >= self.xMax or xRef < self.xMin or \
                yRef >= self.yMax or yRef < self.yMin):
                    return False
                    
            'Find if there is a collision on this tile'
            if self.lsLocations[xRef][yRef].playerID != 0:
                if self.lsLocations[xRef][yRef].isReal:
                    return False
                
            'Find if there is a cardinally adjacent piece of the same type'
            lsEdges = [
                self.lsLocations[xRef+w][yRef+z]
                for w,z in lsCardinalOffsets]
                    
            for tile in lsEdges:
                if tile.playerID == gp.playerID:
                    if tile.isReal:
                        return False
            'Find if there is a diagonally adjacent piece of the same type'

            if not blnValidDiagonalPiece:
                lsCorners = [
                    self.lsLocations[xRef+w][yRef+z]
                    for w,z in lsDiagonalOffsets]
            
                for tile in lsCorners:
                    if tile.playerID == gp.playerID:
                        if tile.isReal:
                            blnValidDiagonalPiece = True
                  
        'If we made it this far, return the valid of valid diagonal piece'
        return blnValidDiagonalPiece
        
    def CheckForValidMoves(self, gamepiece):
        """ Checks to see if a piece can make any valid moves
        
        Arguments:
            gp: A game piece
        """
        gp = gamepiece.copy()
        for x in range(self.xMin, self.xMax):
            for y in range(self.yMin, self.yMax):
                pt = P.point(x,y)
                for j in range(0,2):
                    for i in range(0,4):
                        if self.ValidToPlacePiece(pt, gp):
                            print("player: %s, x: %s, y: %s"%(gp.playerID, pt.x,pt.y))
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

    