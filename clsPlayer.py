# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 19:58:50 2017

@author: Isik
"""
import clsGamePiece as GP
import GamePieceLocationMaps as GPLM

class Player:
    """ Represents a player.
    
    Players have IDs.
    
    Attributes: 
        playerID: 
            An integer (1-4) that represents the player.
        name: 
            A string that is the player's name.
        lsPieces: 
            A vector of all the game pieces.
        points: 
            An integer of the number of points the 
            player has (usually 0)
        blnNoPiecesRemaining: 
            A scorekeeping variable, to detect if all 
            pieces have been used.
        blnLastPieceMonomino: 
            A scorekeeping variable, to detect if the 
            last piece was a monomino.
        blnFirstMove: 
            Indentifies whether this is the player's 
            first move or not. 
    """  
    
    lsPieces = GPLM.lsPieces
    blnLastPieceMonomino = False
    blnNoPiecesRemaining = False
    blnFirstMove = True
    blnDone = False
    
    points = 0
    
    def __init__(self, playerID, name = ""):
        self.playerID = playerID
        self.name = name
        
        'Give default player name if no name was defined'
        if self.name == "":
            self.name = "Player{0}".format(playerID)
        
        'Initialize player pieces'
        self.lsPlayerPieces = [
            GP.GamePiece(piece, self.playerID)
            for piece in self.lsPieces]

        self.SelectedPiece = self.lsPlayerPieces[0]        
        
    def SelectPiece(self, Index):
        """ Sets SelectedPiece by looking for an unselected piece of a players'
        
        Starts looking at an index, if there remains an unselected piece owned
        by the player but this is not that piece, it tries the next.
        
        Arguments:
            Index: The spot in lsPlayerPieces to check for a usable piece.
        """
        if not self.blnNoPiecesRemaining:
            SelectedPiece = self.lsPlayerPieces[Index]
            if not SelectedPiece.used:
                self.SelectedPiece = SelectedPiece
            else:
                self.SelectPiece((Index + 1) % len(self.lsPieces))
            
    def CheckRemainingPieces(self):
        """ 
        Sets blnLastPieceMonomino and blnNoPiecesRemaining based on
        the number of remaining pieces. 
        """
        lsUnusedPieces = []
        for piece in self.lsPlayerPieces:
            if not piece.used:
                lsUnusedPieces.append(piece)
        if len(lsUnusedPieces) == 1:
            if len(lsUnusedPieces[0].lsLocations) == 1:
                self.blnLastPieceMonomino = True
        if len(lsUnusedPieces) == 0:
            self.blnNoPiecesRemaining = True
            
    def SelectNextPiece(self):
        """ Selects the next valid piece """
        CurrentIndex = self.lsPlayerPieces.index(self.SelectedPiece)
        self.SelectPiece((CurrentIndex + 1) % len(self.lsPieces))
            
    def copy(self):
        """ Returns a non-referenced copy of the Player """
        p = Player(self.playerID, self.name)          
        p.lsPlayerPieces = [gp.copy() for gp in self.lsPlayerPieces]
        
        PlayerPieceIndex = self.lsPlayerPieces.index(self.SelectedPiece)
        p.SelectedPiece = p.lsPlayerPieces[PlayerPieceIndex]
        
        p.blnLastPieceMonomino = self.blnLastPieceMonomino
        p.blnNoPiecesRemaining = self.blnNoPiecesRemaining
        p.blnFirstMove = self.blnFirstMove
        
        p.blnDone = self.blnDone
        
        p.points = self.points
        return p