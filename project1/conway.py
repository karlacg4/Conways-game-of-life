"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import datetime

ON = 255
OFF = 0
vals = [ON, OFF]

input = "input5.txt"
output = "output5.txt"

#Still figures
block = np.array([[0,0,0,0],[0,255,255,0],[0,255,255,0],[0,0,0,0]]) #4x4
beehive = np.array([[0,0,0,0,0,0],[0,0,255,255,0,0],[0,255,0,0,255,0],[0,0,255,255,0,0],[0,0,0,0,0,0]]) #5x6
loaf = np.array([[0,0,0,0,0,0],[0,0,255,255,0,0],[0,255,0,0,255,0],[0,0,255,0,255,0],[0,0,0,255,0,0],[0,0,0,0,0,0]]) #6x6
boat = np.array([[0,0,0,0,0],[0,255,255,0,0],[0,255,0,255,0],[0,0,255,0,0],[0,0,0,0,0]]) #5x5
tub = np.array([[0,0,0,0,0],[0,0,255,0,0],[0,255,0,255,0],[0,0,255,0,0],[0,0,0,0,0]]) #5x5

#Oscilators
blinker1 = np.array([[0,0,0],[0,255,0],[0,255,0],[0,255,0],[0,0,0]]) #5x3
blinker2 = np.array([[0,0,0,0,0],[0,255,255,255,0],[0,0,0,0,0]]) #3x5

toad1 = np.array([[0,0,0,0,0,0],[0,0,0,255,0,0],[0,255,0,0,255,0],[0,255,0,0,255,0],[0,0,255,0,0,0],[0,0,0,0,0,0]]) #6x6
toad2 = np.array([[0,0,0,0,0,0],[0,0,255,255,255,0],[0,255,255,255,0,0],[0,0,0,0,0,0]]) #4x6

beacon1 = np.array([[0,0,0,0,0,0],[0,255,255,0,0,0],[0,255,255,0,0,0],[0,0,0,255,255,0],[0,0,0,255,255,0],[0,0,0,0,0,0]]) #6x6
beacon2 = np.array([[0,0,0,0,0,0],[0,255,255,0,0,0],[0,255,0,0,0,0],[0,0,0,0,255,0],[0,0,0,255,255,0],[0,0,0,0,0,0]]) #6x6

#Spaceships
glider1 = np.array([[0,0,0,0,0],[0,0,255,0,0],[0,0,0,255,0],[0,255,255,255,0],[0,0,0,0,0]]) #5x5
glider2 = np.array([[0,0,0,0,0],[0,255,0,255,0],[0,0,255,255,0],[0,0,255,0,0],[0,0,0,0,0]]) #5x5
glider3 = np.array([[0,0,0,0,0],[0,0,0,255,0],[0,255,0,255,0],[0,0,255,255,0],[0,0,0,0,0]]) #5x5
glider4 = np.array([[0,0,0,0,0],[0,255,0,0,0],[0,0,255,255,0],[0,255,255,0,0],[0,0,0,0,0]]) #5x5

ship1 = np.array([[0,0,0,0,0,0,0],[0,255,0,0,255,0,0],[0,0,0,0,0,255,0],[0,255,0,0,0,255,0],[0,0,255,255,255,255,0],[0,0,0,0,0,0,0]]) #6x7
ship2 = np.array([[0,0,0,0,0,0,0],[0,0,0,255,255,0,0],[0,255,255,0,255,255,0],[0,255,255,255,255,0,0],[0,0,255,255,0,0,0],[0,0,0,0,0,0,0]]) #6x7
ship3 = np.array([[0,0,0,0,0,0,0],[0,0,255,255,255,255,0],[0,255,0,0,0,255,0],[0,0,0,0,0,255,0],[0,255,0,0,255,0,0],[0,0,0,0,0,0,0]]) #6x7
ship4 = np.array([[0,0,0,0,0,0,0],[0,0,255,255,0,0,0],[0,255,255,255,255,0,0],[0,255,255,0,255,255,0],[0,0,0,255,255,0,0],[0,0,0,0,0,0,0]]) #6x7

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider


#Posible directions used to check for neighbors
dirs = (
(-1,-1), ( 0,-1), ( 1,-1),
(-1, 0),          ( 1, 0),
(-1, 1), ( 0, 1), ( 1, 1))

#this function counts the neighboprs of a cell
def count(i, j, grid, width, height):
    counts = 0
    for dj,di in dirs:
        if j+dj in range(width) and i+di in range(height) and grid[i+di, j+dj] == ON:
            counts += 1
    return counts

#Creates a list and compares ir with the desired figure to chech if that figure exists
def countFigures(i, j, grid, searchFigure, n1, n2):
    check = grid[i : i + n1 + 1, j : j + n2 + 1]
    if np.array_equal(check, searchFigure):
        return True
    


def update(frameNum, img, grid, width, height):

    cBlock, cHive, cLoaf, cBoat, cTub, cBlinker, cToad, cBeacon, cGlider, cShip  = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    global block, beehive, loaf, boat, tub, blinker1, blinker2, toad1, toad2, beacon1, beacon2, glider1, glider2, glider3, glider4, ship1, ship2, ship3, ship4
    
    global aux
    if aux:
        aux = False
        return
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    padGrid = grid.copy()
    padGrid = np.pad(padGrid, 1, mode = "constant")
    newGrid = grid.copy()
    
    # TODO: Implement the rules of Conway's Game of Life
    for j in range(width):
        for i in range(height):
            c = count(j, i, grid, width, height)
            if grid[j, i] == ON:
                if c < 2 or c > 3:
                    newGrid[j, i] = OFF
            else:
                if c == 3:
                    newGrid[j, i] = ON
            #Check for figures and add to the counter
            if countFigures(j-1, i-1, padGrid, block, 3, 3):
                cBlock +=1
            if countFigures(j-1, i-1, padGrid, beehive, 4, 5):
                cHive +=1
            if countFigures(j-1, i-1, padGrid, loaf, 5, 5):
                cLoaf +=1
            if countFigures(j-1, i-1, padGrid, boat, 4, 4):
                cBoat +=1
            if countFigures(j-1, i-1, padGrid, tub, 4, 4):
                cTub +=1
            if countFigures(j-1, i-1, padGrid, blinker1, 4, 2) or countFigures(j-1, i-1, padGrid, blinker2, 2, 4):
                cBlinker +=1
            if countFigures(j-1, i-1, padGrid, toad1, 5, 5) or countFigures(j-1, i-1, padGrid, toad2, 3, 5):
                cToad +=1
            if countFigures(j-1, i-1, padGrid, beacon1, 5, 5) or countFigures(j-1, i-1, padGrid, beacon2, 5, 5):
                cBeacon +=1
            if countFigures(j-1, i-1, padGrid, glider1, 4, 4) or countFigures(j-1, i-1, padGrid, glider2, 4, 4) or countFigures(j-1, i-1, padGrid, glider3, 4, 4) or countFigures(j-1, i-1, padGrid, glider4, 4, 4):
                cGlider +=1
            if countFigures(j-1, i-1, padGrid, ship1, 5, 6) or countFigures(j-1, i-1, padGrid, ship2, 5, 6) or countFigures(j-1, i-1, padGrid, ship3, 5, 6) or countFigures(j-1, i-1, padGrid, ship4, 5, 6):
                cShip +=1
    
    total = cBlock + cHive + cLoaf + cBoat + cTub + cBlinker + cToad + cBeacon + cGlider + cShip
    miau = False
    if total == 0:
        miau = True
        total += 1
    #append information to output file
    f = open(output, "a")
    f.write("Iteration: {}\n".format(frameNum))
    f.write("===============================\n")
    f.write("|            | Count | Percent |\n")
    f.write("|Block       | {}   | {}%  |\n".format(cBlock, cBlock * 100 / total))
    f.write("|BeeHive     | {}   | {}%  |\n".format(cHive, cHive * 100 / total))
    f.write("|Loaf        | {}   | {}%  |\n".format(cLoaf, cLoaf * 100 / total))
    f.write("|Boat        | {}   | {}%  |\n".format(cBoat, cBoat * 100 / total))
    f.write("|Tub         | {}   | {}%  |\n".format(cTub, cTub * 100 / total))
    f.write("|Blinker     | {}   | {}%  |\n".format(cBlinker, cBlinker * 100 / total))
    f.write("|Toad        | {}   | {}%  |\n".format(cToad, cToad * 100 / total))
    f.write("|Beacon      | {}   | {}%  |\n".format(cBeacon, cBeacon * 100 / total))
    f.write("|Glider      | {}   | {}%  |\n".format(cGlider, cGlider * 100 / total))
    f.write("|Ship        | {}   | {}%  |\n".format(cShip, cShip * 100 / total))
    f.write("===============================\n")
    if miau:
        total -= 1
    f.write("|Total       | {}   |        |\n".format(total))
    f.close()   
                    
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments
    grid = np.array([])
    f = open(input, "r")
    lines = f.readlines()
    width, height = list(map(int, lines[0].split()))
    grid = np.zeros((width, height))
    gen = int(lines[1])
    for l in lines[2:]:
        x, y = list(map(int, l.split()))
        grid[x, y] = ON    
        
    # set animation update interval
    updateInterval = 50

    #create output file
    f = open(output, "w")
    f.write("Simulation at: "+ str(datetime.datetime.now())+"\n")
    f.write("Universe size: "+ str(width)+ "x"+ str(height)+"\n")
    f.close()

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, width, height),
                                  frames = gen,
                                  interval=updateInterval,
                                  save_count=50,
                                  repeat = False)

    plt.show()

# call main
if __name__ == '__main__':
    aux = True
    main()