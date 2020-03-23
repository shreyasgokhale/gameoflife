#!/usr/bin/env python3

"""
Game of Life Wrapper

@author:  Shreyas Gokhale
@contact: shreyas6gokhale@gmail.com
"""

import time
import curses
import cell
import numpy as np
import json

switcher= {"1": "blinker", "2" : "eater", "3": "beacon", "4": "glider", "5": "glidershooter"}
saveGame = {}

def print_state(screen, matrix):
    for (i,j), value in np.ndenumerate(matrix):
        if(value==1):    
            screen.addstr(j, i, '█')

def initCurses(screen):
    curses.start_color()
    x, y = screen.getmaxyx()
    win1 = curses.newwin(x-5,y, 0, 0)
    win1.keypad(0)
    curses.noecho()
    curses.curs_set(0)
    win1.border(0)
    win1.nodelay(1)
    win2 = curses.newwin(5,y, x-5, 0)
    win2.border(0)
    saveGame["rows"] = y-1 
    saveGame["cols"] = x -6    
    return win1, win2


def askForSaveGame(win2):
    global saveGame
    win2.addstr(1, 1, "Do you want to load savegame.txt? ")
    win2.addstr(2, 1, "Press y for yes or any other key to continue.")
    win2.refresh()
    c = win2.getkey()
    win2.refresh()

    if(c == "y"):
        try:
            with open('savegame.txt', 'r') as savefile:
                saveGame = json.load(savefile)
            return True

        except Exception as e:
            win2.refresh()
            win2.addstr(1, 1, "FILE NOT FOUND !, Starting normally")
            return False
    return False            
   
def askOptions(win2):
    win2.refresh()
    win2.addstr(1, 1, "Select one of the options: ") 
    win2.addstr(2, 1, "1]Blinker  2]Eater 3]Beacon 4]Glider 5]Shooter") 
    win2.addstr(3, 1, "Any other key will generate a random pattern") 
    saveGame["shape"] = win2.getch()
    win2.refresh()
   
    
def refreshDisplay(counter, matrix, win1, win2):
    win1.clear()
    win1.border(0)
    win2.clear()
    win2.addstr(1, 1, "Number of Iterations: ") 
    win2.addstr(2, 1, str(counter)) 
    win2.addstr(3, 1, "Press Q to Quit, S to save state. Any other key to continue!") 
    print_state(win1,matrix)
    win1.refresh()
    win2.refresh()

if __name__ == '__main__':
    screen = curses.initscr()
    win1, win2 = initCurses(screen)
    save_flag = askForSaveGame(win2)
    screen.refresh()
    win1.refresh()
    win2.refresh()
    win2.clrtoeol()
    
    if save_flag is False:
        saveGame["counter"] = 0
        askOptions(win2)
        gol = cell.gameOfLife()
        try:
            gol.newGame(saveGame["rows"],saveGame["cols"],switcher[chr(saveGame["shape"])])
        except KeyError:
            gol.newGame(saveGame["rows"],saveGame["cols"], "random")
    else:
        gol = cell.gameOfLife(saveGame["state"])


    win2.clrtoeol()
    screen.refresh()
    input = True

    while(input):
        input =  False
        screen.refresh()
        gol.refresh()
        refreshDisplay(saveGame["counter"], gol.getMatrix(), win1, win2)
        c = win2.getkey()
        if(c != "q"):
            input = True    
        if(c == "s"):
            mat = gol.getMatrix().tolist()
            saveGame["state"] = mat
            with open('savegame.txt', 'w') as savefile:
                json.dump(saveGame, savefile)
        saveGame["counter"]  += 1
    
    curses.endwin()
    quit()