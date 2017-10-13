# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 23:47:33 2017

@author: Isik
"""
import clsGameState as GS
import tkinter as tk  
import clsPoint as pt

lsPlayerColors = ['','red','blue','green','yellow']
lsGhostColors = ['','red4','RoyalBlue1','PaleGreen1','yellow3']

class GUI:
    """ Graphical User Interface for playing Blokus!
    
    Attributes:
        xLast: The last x position that the GUI registered the user entering.
        yLast: The last y position that the GUI registered the user entering.
        busy: A poor man's attempt to eliminate asynchronous behavior
        root: The base level GUI control.
    """
    xLast = 0 
    yLast = 0
    busy = False
    def keyup(self, event):
        """ Is called when a key is raised. Only pulls on H right now """
        if event.char.upper() == 'H':
            self.GameState = self.PlaceHolder.copy()
            self.PlaceGhostPiece(self.xLast, self.yLast)
            self.busy = False
        return
        
    def keydown(self, event):
        """ Is called when a key is pressed. Pulls on R, S, F, H """
        if not self.busy:
            self.busy = True
            self.GameState = self.BufferGameState.copy()
            if event.char.upper() == 'R':
                self.GameState.ActivePlayer.SelectedPiece.Rotate()
                self.BufferGameState = self.GameState.copy()
                self.PlaceGhostPiece(self.xLast, self.yLast)
                self.busy = False
            if event.char.upper() == 'S':
                self.SelectNextPiece()
                self.BufferGameState = self.GameState.copy()
                self.PlaceGhostPiece(self.xLast, self.yLast)
                self.busy = False
            if event.char.upper() == 'F':
                self.GameState.ActivePlayer.SelectedPiece.Flip()
                self.BufferGameState = self.GameState.copy()
                self.PlaceGhostPiece(self.xLast, self.yLast)
                self.busy = False
            if event.char.upper() == 'H':
                self.PlaceHolder = self.GameState.copy()
                self.GameState = self.BufferGameState.copy()
                self.DisplayBoard()
        return
                
    def buttonpress(self, event):
        """ Is called when a button in the BLOKUS grid is pressed. """
        if not self.busy:
            self.busy = True
            self.GameState = self.BufferGameState.copy()
            self.PlacePiece(self.dtButton[event.widget].x, self.dtButton[event.widget].y)
            self.BufferGameState = self.GameState.copy()
            self.busy = False
        return
        
    def enter(self, event):
        """ Is called when the mouse enters a button in the BLOKUS grid """
        if not self.busy:
            self.busy = True
            self.xLast = self.dtButton[event.widget].x
            self.yLast = self.dtButton[event.widget].y
            self.PlaceGhostPiece(self.xLast, self.yLast)
            self.busy = False
        return
        
    def leave(self, event):
        """ Is called when the mouse leaves a button """
        if not self.busy:
            self.busy = True
            self.GameState = self.BufferGameState.copy()
            self.busy = False
        return
        
    def __init__(self):
        self.GameState = GS.GameState(4)
        self.BufferGameState = self.GameState.copy()
        self.PlaceHolder = self.GameState.copy()
        
        self.xLastMin = self.GameState.GameBoard.xMin
        self.xLastMax = self.GameState.GameBoard.xMax
        self.yLastMin = self.GameState.GameBoard.yMin
        self.yLastMax = self.GameState.GameBoard.yMax


        'Here we load the entire control'
        self.dtButton = dict()
        self.root = tk.Tk(  )
        self.root.bind('<KeyPress>', self.keydown)
        self.root.bind('<KeyRelease>', self.keyup )
        for x in range(self.xLastMin, self.xLastMax):
            for y in range(self.yLastMin, self.yLastMax): 
                frame = tk.Frame(self.root, width=40, height=40)
                button = tk.Button(frame, text="",)
                frame.grid_propagate(False)
                frame.columnconfigure(0, weight=1)
                frame.rowconfigure(0, weight=1)       
                frame.grid(row=x, column=y)
                button.grid(sticky="wens")
                button.bind('<Enter>',self.enter)
                button.bind('<Leave>',self.leave)
                button.bind('<ButtonPress>',self.buttonpress)
                self.dtButton[button]= pt.point(x,y)
        
        lsPlayerColors[0] = self.root.cget("bg")
        lsGhostColors[0] = lsPlayerColors[0]
        
        self.DisplayBoard()
        self.root.mainloop(  )   
        
        
        
        
    def DisplayTurn(self):
        """ Dummy function. Tells the user which player's turn it is """
        print("It is {0}'s turn!".format(self.GameState.ActivePlayer.name))
        
    def DisplayBoard(self, blnGhost = False):
        lsPlayableLocations = self.GameState.GameBoard.lsLocations
        for button in self.dtButton.keys():
            btnX = self.dtButton[button].x
            btnY = self.dtButton[button].y
            Tile = lsPlayableLocations[btnX][btnY]
            if Tile.isGhost:
                color = lsGhostColors[Tile.playerID]
            else:
                color = lsPlayerColors[Tile.playerID]
            button.configure(bg = color)
            
                
    def SelectNextPiece(self):
        """ Function here because sometimes I care about abstraction """
        self.GameState.SelectNextPiece()
        
    def PlacePiece(self, x, y):
        """ Places a piece I'm tired comments suck """
        success = self.GameState.PlacePiece(x, y)
        if not success:
            self.PlaceGhostPiece(x,y)

        self.DisplayTurn()
        self.DisplayBoard()
        
        if not success:
            self.GameState = self.BufferGameState.copy()

        if self.GameState.GameOver:
            self.EndGame()
        
    def PlaceGhostPiece(self, x, y):
        """ Oh my god just leave me alone """
        self.GameState.PlacePiece(x, y, True)
        self.DisplayBoard(True)
        
    def EndGame(self):
        """GAME OVER NERDS"""
        print("GAME OVER NERDS")
        print("PLAYER ONE EARNED %s POINTS:"%self.GameState.lsPlayer[0].points)
        print("PLAYER TWO EARNED %s POINTS:"%self.GameState.lsPlayer[1].points)
        print("PLAYER THR EARNED %s POINTS:"%self.GameState.lsPlayer[2].points)
        print("PLAYER FOU EARNED %s POINTS:"%self.GameState.lsPlayer[3].points)
