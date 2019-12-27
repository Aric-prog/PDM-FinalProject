import os
clear = lambda : os.system('cls')

height : int = 3
width  : int = 3

grid = [["-" for x in range(width)] for y in range (width)]

def displayGrid():
    # Temporarily here
    count = 0
    space = "  "
    print("+",end="\t")
    for i in range(width):
        if((i)>=10):
            space=" "
        print(i, end = space)

    print()
    for i in grid:
        print(count,end="\t")
        count+=1
        for j in i:
            print(j,end = "  ")
        print()

def setLive(x,y):
    grid[x][y] = "X"


# returns a list of neighbouring coordinates of the selected point
def neighbourIterator(yCoord,xCoord) -> list:
    neighbourCoordinates = []
    yCoord -= 1
    xCoord -= 1
    for y in range(3):
        for x in range(3):
            if((yCoord+y<0 or yCoord+y>height-1) or (xCoord+x<0 or xCoord+x>width-1)):
                continue
            neighbourCoordinates.append([yCoord+y,xCoord+x])

    # deletes the source coordinate, since that isn't a part of the neighbouring cell
    neighbourCoordinates.remove([yCoord+1,xCoord+1])
    
    return neighbourCoordinates


# returns an integer of surrounding live cell
def neighbourCounter(yCoord,xCoord) -> int:
    liveNeighbour = 0
    for neighbour in neighbourIterator(yCoord,xCoord):
        if(grid[neighbour[0]][neighbour[1]] == "X"):
            liveNeighbour += 1
    return liveNeighbour

# runs the main loop to add cells that are alive    
while True:
    clear()

    print("1. Input live cell")
    print("2. Simulate next step")

    option = int(input("Pick option no : "))
    if(option == 1):
        try:
            a = int(input("Put in col no : "))
            b = int(input("Put in row no : "))

            # checks if the input is valid, border is subtracted by 1 to account for the array
            if((a<0 or a>height-1) or (b<0 or b>width-1)):
                print("Invalid Input")
                input("Press Enter to continue")
                clear()
                continue

            setLive(a,b)
        except:
            print("Invalid Input")
            input("Press Enter to continue")
            clear()
            continue

    elif(option == 2):
        nextGrid = []
        print(id(nextGrid),id(grid))
        for y in range(height):
            nextGrid.append([])
            for x in range(width):
                liveNeighbour = neighbourCounter(y,x)
                
                # checks if a live cell has either 2 or 3 live neighbours
                if(grid[y][x] == "X" and liveNeighbour in range(2,4)):
                    nextGrid[y].append("X")
                    continue
                elif(grid[y][x] == "-" and liveNeighbour == 3):
                    nextGrid[y].append("X")
                    continue
                else:
                    nextGrid[y].append("-")
                    continue
        grid = nextGrid[:]
    displayGrid()
    input("Press Enter to continue")

displayGrid()

