import os
import pygame
import grid as g
import time

clear = lambda : os.system('cls')

# grids will contain grid objects
grids = []

WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
                
# creates a grid object
def initializeNewGrid():
    gridDatas = {}
    dataKeywords = ['gridHeight','gridWidth','cellSize']

    # creates a dictionary, with the key originating from dataKeywords
    # this dictionary will then be used as a keyword argument
    for keyword in dataKeywords:
        dataEntered = False
        while not dataEntered:
            clear()
            print("Enter 0 for default value")
            
            # checks for invalid input 
            try:
                gridData = int(input("Enter " + keyword[:4] + " " + keyword[4:].lower() + " : "))
                if(gridData != 0):
                    gridDatas[keyword] = gridData
                    dataEntered = True
                else:
                    dataEntered = True
            except:
                continue
    
    # creates a grid object, with the information provided by the dictionary
    grids.append(g.grid(**gridDatas))

# runs the main loop
while True:
    clear()
    print("What would you like to do : ")
    print("1. Add new grid")
    print("2. View grids")

    try:
        option = int(input("Option no : "))
        assert(option <= 2)
        if(option == 1):
            clear()
            initializeNewGrid()
            grids[-1].setupGrid()    
        elif(option == 2 and len(grids) != 0):
            break
        else:
            print("Grid is empty")
            input("Press Enter to continue")
            continue
    except AssertionError:
        print("Invalid input")

# initializes pygame
def pygameDisplay():
    pygame.init()
    done = False
    tick = 0
    clock = pygame.time.Clock()
    
    gridsIndex = 0
    
    # gets all of the data from the selected grid
    gridArr = grids[gridsIndex].gridArr
    gridWidth  = grids[gridsIndex].gridWidth
    gridHeight = grids[gridsIndex].gridHeight
    cellSize   = grids[gridsIndex].cellSize
    cellMargin = grids[gridsIndex].cellMargin
    cellWithMargin = cellSize + cellMargin
    
    while not done:
        startTime = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # if space is pressed, change the grid
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gridsIndex = gridsIndex + 1 if gridsIndex < len(grids)-1 else 0
                
                # gets all of the data from the selected grid
                gridArr = grids[gridsIndex].gridArr
                gridWidth  = grids[gridsIndex].gridWidth
                gridHeight = grids[gridsIndex].gridHeight
                cellSize   = grids[gridsIndex].cellSize
                cellMargin = grids[gridsIndex].cellMargin
                cellWithMargin = cellSize + cellMargin

        # calculates the size of the screen thats going to be displayed
        screenWidth = gridWidth * (cellWithMargin)
        screenHeight = gridHeight * (cellWithMargin)
        screen = pygame.display.set_mode((screenWidth,screenHeight))
        
        # fills the background
        screen.fill(WHITE)

        # added 1 so that the lines create a proper square.
        # draws the line that separate the cells
        verticalLinesDrawn = False
        for y in range(gridHeight + 1):
            # used so that the program doesn't keep creating vertical lines for every cell, only drawing it once
            if(not verticalLinesDrawn):
                for x in range(gridWidth + 1):
                    pygame.draw.line(screen , BLACK , (x * cellWithMargin,0) , (x * cellWithMargin ,screenHeight))
            verticalLinesDrawn = True
            pygame.draw.line(screen , BLACK , (0,y * cellWithMargin) , (screenWidth,y * cellWithMargin))

        # draws the cell into display
        for y in range(gridHeight):
            for x in range(gridWidth):
                if(gridArr[y][x]):
                    pygame.draw.rect(screen,GREEN,(cellWithMargin * x + cellMargin, cellWithMargin * y + cellMargin,cellSize,cellSize))
                    continue
        
        # for every second, adds the number of generation, and gets the next generation of grid
        tick += 1
        simulationInterval = 60
        if(tick % simulationInterval == 0):
            tick = 0
            # calculates the next generation of grid and replaces the old one
            gridArr = grids[gridsIndex].nextGeneration()
            grids[gridsIndex].gridArr = gridArr

        clock.tick(60)

        # displays the fps on the caption
        fps = 1 / (time.time() - startTime)
        pygame.display.set_caption("Conway's Game of Life. FPS: "+ (str(fps)))
        pygame.display.flip()
    pygame.quit()
pygameDisplay()