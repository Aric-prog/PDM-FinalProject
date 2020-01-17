class grid:
    def __init__(self,gridHeight = 16,gridWidth = 16,cellSize = 20):
        self.gridWidth  : int = int(gridWidth)
        self.gridHeight : int = int(gridHeight)
        self.gridArr = [[0 for x in range(self.gridWidth)] 
                        for y in range (self.gridHeight)]
        self.cellSize  = cellSize
        self.cellMargin = 1

    def displayConsoleGrid(self):
        # displays the grid on the console
        count = 0
        space = "  "
        print(" ",end="\t")
        # displays the horizontal numbers, indicating the rows
        for i in range(self.gridWidth):
            # reduces the space if the number is bigger or equal than 10
            if(i >= 10):
                space = " "
            print(i, end = space)

        print()
        for i in self.gridArr:
            # shows the vertical number indicating the columns
            print(count,end="\t")
            count += 1

            # prints all of the element in the gridArr
            for j in i:
                if(j):
                    print("*",end = "  ")
                else:
                    print("-",end = "  ")
            print()
            
    def setLive(self,x,y):
        self.gridArr[x][y] = 1

    # returns a list of neighbouring coordinates of the selected point
    def neighbourIterator(self,yCoord,xCoord) -> list:
        # Initializes an empty list that contains the neighbour coordinates
        neighbourCoordinates = []
        # Initializes neighbour range, this will be used to iterate through all of the neighbouring cell
        neighbourRange = 3
        yCoord -= 1
        xCoord -= 1

        # Indexes through the neighbouring range, starting from top left (-1,-1 coordinate from origin)
        # and ending at bottom right (+1,+1 coordinate from origin)
        for y in range(neighbourRange):
            for x in range(neighbourRange):
                # This will check if a neighbour is viable (not resulting in IndexError of gridArr). And if it is, it will append it
                # to neighbourCoordinates
                if((yCoord + y < 0 or yCoord + y > self.gridHeight-1) or (xCoord + x < 0 or xCoord + x > self.gridWidth - 1)):
                    continue
                neighbourCoordinates.append([yCoord + y,xCoord + x])

        # deletes the source coordinate, since that isn't a part of the neighbouring cell
        neighbourCoordinates.remove([yCoord + 1,xCoord + 1])

        return neighbourCoordinates

    # returns an integer of surrounding live cell
    def neighbourCounter(self,yCoord,xCoord):
        liveNeighbour = 0
        for neighbour in self.neighbourIterator(yCoord,xCoord):
            if(self.gridArr[neighbour[0]][neighbour[1]] == 1):
                liveNeighbour += 1
        return liveNeighbour

    def nextGeneration(self):
        nextGrid = []
        for y in range(self.gridHeight):
            nextGrid.append([])
            for x in range(self.gridWidth):
                liveNeighbour = self.neighbourCounter(y,x)
                # checks if a live cell has either 2 or 3 live neighbours
                if(self.gridArr[y][x] == True and liveNeighbour in range(2,4)):
                    nextGrid[y].append(1)
                    continue
                elif(self.gridArr[y][x] == False and liveNeighbour == 3):
                    nextGrid[y].append(1)
                    continue
                else:
                    nextGrid[y].append(0)
                    continue
        return nextGrid

    def reader(self,filename):
        # reads a txt file and returns it as a replacement grid
        # also updates the gridWidth and gridHeight

        # checks if the filename is valid, if not, return the previous value
        try:
            txtfile = open("Configs\\" + filename+ ".txt",'r')
        except:
            return self.gridArr

        with open("Configs\\" + filename+".txt",'r') as txtfile:
            # reads the file into a list, separated by lines
            lines = txtfile.readlines()

            # removes \n from the lines, and creates a separates the elements per line
            # for example ["0,0,0"] will become [0,0,0] with each 0 being a different element instead of one string
            newGrid = [lines[n].replace("\n","").split(',') for n in range(len(lines))]

            # indexes through all the elements in newGrid
            for y in range(len(newGrid)):
                for x in range(len(newGrid[y])):
                    # changes the element inside to be an integer
                    newGrid[y][x] = int(newGrid[y][x])
                    
        self.gridWidth  = len(newGrid[0])
        self.gridHeight = len(newGrid)
        return newGrid

    # runs the loop to add live cells or read from file
    def setupGrid(self):
        while True:

            print("1. Input live cell")
            print("2. Read from file")
            print("3. Finish")
            
            # display the grid on console
            self.displayConsoleGrid()
            option = int(input("Pick option no : "))

            if(option == 1):
                try:
                    a = int(input("Put in col no : "))
                    b = int(input("Put in row no : "))

                    assert(isinstance(a,int) and isinstance(b,int))
                    # checks if the input is valid, and not exceeding the array index, border is subtracted by 1 to account for the array
                    assert((not (a < 0 or a > self.gridHeight-1)) or (not (b < 0 or b > self.gridWidth-1)))
                    self.setLive(a,b)

                except AssertionError:
                    clear()
                    print("Invalid Input")
                    input("Press Enter to continue")
                    continue
                
            # prompts the user to insert the name of the file,and replaces the grid with the one read
            elif(option == 2):
                filename = str(input("Insert filename (file must be .txt extension) : "))
                self.gridArr = self.reader(filename)
            
            elif(option == 3):
                break