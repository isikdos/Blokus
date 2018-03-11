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
    GAMEOVER = False
    
    
    def begingame(self, event):
        """ Beings the game based on the contents of GameStartText """
        for btn in self.dtButton.keys():
            btn.configure(bg = lsPlayerColors[0])
        self.GameState = GS.GameState(self.numPlayer.get())
        self.BufferGameState = self.GameState.copy()
        self.PlaceHolder = self.GameState.copy()
        self.DisplayTurn()
            
    
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
            
        GameFrame = tk.Frame(self.root, width = 800, height = 800)
        GameFrame.grid(row = 1, column = 1)
        PlayerFrame = tk.Frame(self.root, width = 125)
        
        PlayerFrame.rowconfigure(0, minsize = 200)
        PlayerFrame.rowconfigure(1, minsize = 50)
        PlayerFrame.rowconfigure(2, minsize = 100)
        PlayerFrame.rowconfigure(3, minsize = 100)
        PlayerFrame.rowconfigure(4, minsize = 100)        
        PlayerFrame.rowconfigure(5, minsize = 100)
        PlayerFrame.columnconfigure(0, minsize = 125)

        txtActive = tk.Label(PlayerFrame, text = "ACTIVE PLAYER")
        txtActive.grid(row = 1, column = 0)        
        
        self.Player1 = tk.Frame(PlayerFrame, width = 100, height = 200)
        self.Player1.grid(row = 2, column = 0)
        
        self.Player2 = tk.Frame(PlayerFrame, width = 100, height = 200)
        self.Player2.grid(row = 3, column = 0)        
        
        self.Player3 = tk.Frame(PlayerFrame, width = 100, height = 200)
        self.Player3.grid( row = 4, column = 0)
        
        self.Player4 = tk.Frame(PlayerFrame, width = 100, height = 200)
        self.Player4.grid( row = 5, column = 0)
        
        GameStartButtonFrame = tk.Frame(PlayerFrame, width = 100, height = 200)
        GameStartButtonFrame.grid( row = 0, column = 0)
        
        GameStartButton = tk.Button(GameStartButtonFrame, text = "START")
        GameStartButton.grid( row = 0, column = 0)
        
        self.numPlayer = tk.IntVar(GameStartButtonFrame, 4)
        self.GameStartText = tk.OptionMenu(GameStartButtonFrame, self.numPlayer, 4, 3, 2)
        self.GameStartText.grid( row = 2, column = 0)
        
        self.PlayerPoints1 = tk.StringVar(GameStartButtonFrame, "")
        self.PlayerPoints2 = tk.StringVar(GameStartButtonFrame, "")
        self.PlayerPoints3 = tk.StringVar(GameStartButtonFrame, "") 
        self.PlayerPoints4 = tk.StringVar(GameStartButtonFrame, "")        
        
        
        txtPlayer1 = tk.Label(self.Player1, width = 10, text = "PLAYER 1", anchor = 'w')
        txtPlayer1.pack()
        self.TextBoxPlayer1 = tk.Label(self.Player1, width = 10, textvar = self.PlayerPoints1, anchor = 'w')
        self.TextBoxPlayer1.pack()
        
        txtPlayer2 = tk.Label(self.Player2, width = 10, text = "PLAYER 2", anchor = 'w')
        txtPlayer2.pack()
        self.TextBoxPlayer2 = tk.Label(self.Player2, width = 10, textvar = self.PlayerPoints2, anchor = 'w')
        self.TextBoxPlayer2.pack()
        
        txtPlayer3 = tk.Label(self.Player3, width = 10, text = "PLAYER 3", anchor = 'w')
        txtPlayer3.pack()
        self.TextBoxPlayer3 = tk.Label(self.Player3, width = 10, textvar = self.PlayerPoints3, anchor = 'w')
        self.TextBoxPlayer3.pack()
        
        txtPlayer4 = tk.Label(self.Player4, width = 10, text = "PLAYER 4", anchor = 'w')
        txtPlayer4.pack()
        self.TextBoxPlayer4 = tk.Label(self.Player4, width = 10, textvar = self.PlayerPoints4, anchor = 'w')
        self.TextBoxPlayer4.pack()
        
        self.Player1.configure(highlightbackground = lsPlayerColors[1], highlightcolor = lsPlayerColors[1], highlightthickness = 1)
        self.Player2.configure(highlightbackground = lsPlayerColors[2], highlightcolor = lsPlayerColors[2], highlightthickness = 1)
        self.Player3.configure(highlightbackground = lsPlayerColors[3], highlightcolor = lsPlayerColors[3], highlightthickness = 1)
        self.Player4.configure(highlightbackground = lsPlayerColors[4], highlightcolor = lsPlayerColors[4], highlightthickness = 1)
        
        PlayerFrame.grid(row = 1, column = 0)
        for x in range(self.xLastMin, self.xLastMax):
            for y in range(self.yLastMin, self.yLastMax): 
                frame = tk.Frame(GameFrame, width=40, height=40)
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
        
        GameStartButton.bind('<ButtonPress>', self.begingame)        
        
        self.DisplayBoard()
        self.root.mainloop(  )   
        
        
        
        
    def DisplayTurn(self):
        """ Dummy function. Tells the user which player's turn it is """
        pass
        
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
        if not self.GAMEOVER:
            success = self.GameState.PlacePiece(x, y)
            if not success:
                self.PlaceGhostPiece(x,y)
    
            self.DisplayTurn()
            self.DisplayBoard()
        
        if not success:
            self.GameState = self.BufferGameState.copy()

        self.ReadGameState()
        
    def PlaceGhostPiece(self, x, y):
        """ Oh my god just leave me alone """
        if not self.GAMEOVER:
            self.GameState.PlacePiece(x, y, True)
            self.DisplayBoard(True)
        
    def ReadGameState(self):     
        if self.GameState.GameOver:
            self.EndGame()
        
            
            
    def EndGame(self):
        self.PlayerPoints1.set(self.GameState.lsPlayer[0].points)
        self.PlayerPoints2.set(self.GameState.lsPlayer[1].points)
        if len(self.GameState.lsPlayer) > 2:
            self.PlayerPoints3.set(self.GameState.lsPlayer[2].points)
        if len(self.GameState.lsPlayer) > 3:
            self.PlayerPoints4.set(self.GameState.lsPlayer[3].points)
        self.GAMEOVER = True