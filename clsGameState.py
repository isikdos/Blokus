# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 20:12:42 2017

@author: Isik
"""
import clsPlayer as P
import clsGameBoard as GB
import clsPoint as PT

class GameState:
    """ Manages the progression of the game, independently of the players.
    
    Holds the state of the game. This object is responsible for knowing
        the turn, the active player, and for placing pieces and evaluating
        the board state. This object allows the rest of the objects to ignore
        the actual state of the game.
        
    Attributes:      
        ActivePlayer: A player object that is the player whose turn it is.
        lsPlayer: A list of all players, their indices are their playerID.
        turn: An integer that represent whose turn it is.
        GameBoard: A GameBoard type object.
        GameOver: Keeps track of whether or not the game is over
    """
    
    turn = 0
    GameOver = False
    def __init__(self, numPlayers):
        self.GameBoard = GB.GameBoard() 
        self.numPlayers = numPlayers
        self.lsPlayer = [P.Player(i) for i in range(1, numPlayers+1)] 
        self.ActivePlayer = self.lsPlayer[self.turn].copy()

    def PlacePiece(self, x, y, blnGhostPlacement = False):
        """ Places a piece on the board, either with validation or not.
        
        Given X, Y coordinates a piece is placed on the board for the
        active player. If blnGhostPlacement is high then it does not check
        to see if the selected place is valid for placement, it just places it.
        """
        point = PT.point(x,y)
        blnSuccess = self.GameBoard.PlacePiece(point, 
                                     self.ActivePlayer.SelectedPiece, 
                                     blnGhostPlacement,
                                     self.ActivePlayer.blnFirstMove)       
        if blnSuccess:                                          
            if not blnGhostPlacement:
                self.ActivePlayer.blnFirstMove = False
                self.ActivePlayer.SelectedPiece.used = True
                self.ActivePlayer.CheckRemainingPieces()
                if not self.ActivePlayer.blnNoPiecesRemaining:
                    self.ActivePlayer.SelectPiece(0)
                self.EvaluateTurn()
                
        return blnSuccess
        
            
    def ChangeTurn(self):
        """ Changes turn to the turn of the next player who can play a piece"""
        self.lsPlayer[self.turn] = self.ActivePlayer.copy()
        self.turn = (self.turn + 1) % self.numPlayers
        self.ActivePlayer = self.lsPlayer[self.turn].copy()
        if not self.CheckForValidMoves(self.ActivePlayer):
            self.ChangeTurn()
        
    def CheckForValidMoves(self, player = None):
        """ Checks if a player has any playable pieces remaining """
        if player is None:
            player = self.ActivePlayer
        if not player.blnDone:
            for piece in player.lsPlayerPieces:
                if not piece.used:
                    if self.GameBoard.CheckForValidMoves(piece, 
                                                         player.blnFirstMove):
                        return True
                        
        player.blnDone = True
        return False
            
    def EndGame(self):
        """ Evaluates the end of the game by computing points """
        for player in self.lsPlayer:
            player.points = self.GameBoard.numPlayerTiles(player.playerID)
            if player.blnNoPiecesRemaining:
                if player.blnLastPieceMonomino:
                    player.points += 20
                else:
                    player.points += 15
   
    def CheckForGameOver(self, n = 0):
        """ Checks to see if the game is over eg: No more plays are possible"""
        if n == self.numPlayers:
            self.GameOver = True
            return
        player = self.lsPlayer[n]
        if player.blnNoPiecesRemaining:
            self.CheckForGameOver(n + 1)
        if not self.CheckForValidMoves(player):
            self.CheckForGameOver(n + 1)
            
    def EvaluateTurn(self):
        """ 
        Checks to see if the game should be ended or if the turn should
        be changed.
        """        
        self.CheckForGameOver()
        if self.GameOver:
            self.EndGame()
        else:
            self.ChangeTurn()
    
    def SelectNextPiece(self):
        """ Selects the ActivePlayer's next piece """
        self.ActivePlayer.SelectNextPiece()

    def copy(self):
        """ Creates a non-referenced copy of game state """
        gs = GameState(self.numPlayers)        
        gs.lsPlayer = [player.copy() for player in self.lsPlayer]
        gs.turn = self.turn
        gs.ActivePlayer = gs.lsPlayer[gs.turn]
        gs.GameBoard = self.GameBoard.copy()
        gs.GameOver = self.GameOver
        return gs
        
            
                                             
        
        