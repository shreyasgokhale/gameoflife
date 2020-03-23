#!/usr/bin/env python3

"""
Module representing one cell for Conway's Game of Life

Rules:
Any live cell with fewer than two live neighbours dies, as if by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

@author:  Shreyas Gokhale
@contact: shreyas6gokhale@gmail.com
"""

import numpy as np

class gameOfLife:
    
    def __init__(self, state = None):
        if state:
            self.board = np.array(state)

    def printBoard(self):
        print(self.board)
    
    def testGame(self, testname, size_x, size_y):
        self.board = np.zeros((size_x, size_y), dtype=int)
        i = 4
        j = 4

        if testname is "random":
            self.board = np.random.randint(0, 2, (size_x,size_y))
   
        if testname is "blinker":
            self.board[i,j:j+3] = 1 
        
        elif testname is "eater":
            self.board[i,j] = 1
            self.board[i+1,j] = 1
            self.board[i,j+1] = 1
            self.board[i+3,j+1:j+4] = 1
            self.board[i+4,j+3] = 1

        elif testname is "beacon":
            self.board[i:i+2,j:j+2] = 1
            self.board[i+2:i+4,j+2:j+4] = 1 
    
        elif testname is "glider":        
            glider = np.array([[0,0,1],[1,0,1],[0,1,1]]) 
            self.board[i:i+3, j:j+3] = glider 
    
        elif testname is "glidershooter":
            i = 0
            j = 0
            shooter = np.zeros(11*38).reshape(11, 38)
            shooter[5][1] = shooter[5][2] = 1
            shooter[6][1] = shooter[6][2] = 1
            shooter[3][13] = shooter[3][14] = 1
            shooter[4][12] = shooter[4][16] = 1
            shooter[5][11] = shooter[5][17] = 1
            shooter[6][11] = shooter[6][15] = 1
            shooter[6][17] = shooter[6][18] = 1
            shooter[7][11] = shooter[7][17] = 1
            shooter[8][12] = shooter[8][16] = 1
            shooter[9][13] = shooter[9][14] = 1
            shooter[1][25] = 1
            shooter[2][23] = shooter[2][25] = 1
            shooter[3][21] = shooter[3][22] = 1
            shooter[4][21] = shooter[4][22] = 1
            shooter[5][21] = shooter[5][22] = 1
            shooter[6][23] = shooter[6][25] = 1
            shooter[7][25] = 1
            shooter[3][35] = shooter[3][36] = 1
            shooter[4][35] = shooter[4][36] = 1   
            self.board[i:i+11, j:j+38] = shooter 

    def getMatrix(self):
        return self.board
        
    def newGame(self, size_x, size_y, pattern):
        self.testGame(pattern, size_x, size_y)
 
    def findNeighbourSum(self, x, y):
        mat =  self.board[x-1 : x+2, y-1 : y+2] 
        return np.sum(mat) -  self.board[x,y] 

    def refresh(self):
        new_board = np.zeros(self.board.shape, dtype=int)
        for x,y in np.ndindex(self.board.shape):
            neighbour_sum = self.findNeighbourSum(x,y)
            if(self.board[x,y] == 1):
                # The cell is alive
                if(not (neighbour_sum < 2 or neighbour_sum >3)):
                    # We already have zero filled numpy 
                    new_board[x,y] = 1  # Cell Lives   
            elif(self.board[x,y] == 0):
                # If cell is dead
                if(neighbour_sum == 3):
                    new_board[x,y] = 1 # Cell becomes alive!
        self.board = new_board
