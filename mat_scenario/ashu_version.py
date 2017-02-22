def maxXcord(coords = []): #prints the max x coordinate in the list
    return max(coords, key=lambda item:item[0])[0]

def maxYcord(coords = []): #prints the max Y coordinate in the lsit
    return max(coords, key=lambda item:item[1])[0]

def minXcord(coords = []): #prints the max x coordinate in the list
    return min(coords, key=lambda item:item[0])[0]

def minYcord(coords = []): #prints the max x coordinate in the list
    return min(coords, key=lambda item:item[1])[0]

def assignCoords(squares = {}, coords = [], maxX, maxY, minX, minY):
    #do i make new lists for every key in the dictionary? - guess i answered my own question
    sq1 = []
    sq2 = []
    sq3 = []
    sq4 = []
    for x in coords:
        if(x[0] in range(minX , 0) and x[1] in range(0,maxY)):
            squares[0] = sq1.append(x)
        if(x[0] in range(0,maxX) and x[1] in range(0,maxY)):
            squares[1] = sq2.append(x)
        if(x[0] in range(0,maxX and x[1] in range(minY, 0))):
            squares[2] = sq3.append(x)
        if(x[0] in range(minX, 0) and x[1] in range(minY,0)):
            squares[3] = sq4.append(x)
    return squares

def awaken(squareNo, first, coordinates = [], gridAllocation = {}):
    i = 0
    unvisited = set(coordinates[:])  #sets don't preserve elements in order- be careful frand
    #visited = set([[]])
    path = []
    unvisited.remove(start)
    path.append([start]) #creating a nested list here
    while(gridAllocation[squareNo][1] != first):
        second = gridAllocation[squareNo][1] #picking any random coordinate that's not the first one
    unvisited.remove(second)
    path[i].append(second)
    path.append([second])
    i++
    for x in gridAllocation[squareNo]:
       unvisited.remove(x)
       path[i].append(x)
    return path

    

coordinates = [(0,0),(10,10),(8,10),(9,9),(5,0),(0,7),(1,8)]
unvisited = set(coordinates[:]) #duplicating the coordinates list
visited = set() #creating an empy set of visited
gridAllocation = {} #empty dictionary for grid allocation
path = [[]] #nested list for the path of every robot
firstCoord = (0,0) #need the first coordinate
#getting the size of the grid
maxX = maxXcord(coordinates)
maxY = maxYcord(coordinates)
minX = minX(coordinates)
minY = minY(coordinates)


    
    


