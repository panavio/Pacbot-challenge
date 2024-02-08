# You can modify this file to implement your own algorithm

from constants import *
import math
"""
You can use the following values from constants.py to check for the type of cell in the grid:
I = 1 -> Wall 
o = 2 -> Pellet (Small Dot)
e = 3 -> Empty
"""
"""
Calculate the next coordinate for 6ix-pac to move to.
Check if the next coordinate is a valid move.

Parameters:
- grid (list of lists): A 2D array representing the game board.
- location (list): The current location of the 6ix-pac in the form (x, y).

Returns:
- list or tuple: 
    - If the next coordinate is valid, return the next coordinate in the form (x, y) or [x,y].
    - If the next coordinate is invalid, return None.
"""



def check_intersection(grid, location):
    x=location[0]
    y=location[1]
    directions = {
        "left":(x-1,y), 
        "right":(x+1,y),
        "up":(x,y-1),
        "down":(x,y+1)}

    valdir = []
    for dirtest in directions:
        a=directions[dirtest][0]
        b=directions[dirtest][1]
        cell=grid[a][b] 
        if cell!= I:
            #print(dirtest + " is valid" + str(directions[dirtest]))
            valdir.append(dirtest)
    #print(valdir)
    return valdir

def check_branch(grid, location):
    if len(check_intersection(grid, location)) > 2:
        return True
    else:
        return False
    
global steps
steps = []

def check_loop(grid, path, nextdir):
    count = 0
    for i in range(len(path) - 1):
        if path[i:i + 2] == [path[-1], nextdir]:
            count += 1
            if count >= (len(grid)/5): #yg ini bisa diubah kalo lebih kecil makin dilimit
                return True
            
    if len(path) >= 2:
        if path[-2] == nextdir:
            return True
    return False

    
#path is saved path
#steps is future path
def scan_map(grid, location, path, pellets):
    
    if len(path) >= (len(grid) * len(grid[0]))/2:
        return [] 

    if pellets == []:
        return [location]

    x=location[0]
    y=location[1]
    directions = {
            "left":(x-1,y), 
            "right":(x+1,y),
            "up":(x,y-1),
            "down":(x,y+1)}

    valdir = check_intersection(grid, location)

    steps=[]
    #set step for valid direction number 1
    if check_loop(grid, path, directions[valdir[0]]):
        if len(valdir) > 1:
            valdir.pop(0)
    pellets_next = pellets.copy()
    if list(directions[valdir[0]]) in pellets:
        pellets_next.remove(list(directions[valdir[0]]))
    steps = scan_map(grid, directions[valdir[0]], path + [directions[valdir[0]]], pellets_next)
    valdir.pop(0)
    #compare with all other valid direction if any of them is shorter
    for dir in valdir:
        if check_loop(grid, path, directions[dir]):
            continue
        else:
            pellets_next = pellets.copy()
            if list(directions[dir]) in pellets:
                pellets_next.remove(list(directions[dir]))
            step2=scan_map(grid, directions[dir], path + [directions[dir]], pellets_next)
            if len(step2) <= len(steps):
                steps = step2

    for box in steps:
        if list(box) in pellets:
            pellets.remove(list(box))

    if(len(steps)>len(path)):
        prefixSteps=steps[0:len(path)]
        if(prefixSteps==path):
            return steps
    else:
        return path + steps
    #print(path+steps)
    return path + steps 


executedOnce=False
output=[]
def get_next_coordinate(grid, location):
    global output
    global executedOnce

    if executedOnce==False:
        pellets = []
        for row in range(len(grid)):
            for column in range(len(grid[row])):
                if grid[row][column] == o:
                    pellets.append([row, column])
        if pellets == []:
            return None
        output = []
        #return location
        output = scan_map(grid, location, [location], pellets)
        if output == []:
            return None
        print(output)
        c=len(output)
        n=(-1 + (1 ** 2 + 4 * 1 * c) ** 0.5)/2
        n=math.ceil(n)+2
        print(n)
        #output=output[-n:]
        #for i in range(len(path) - 1):
        #if output[i:i + n-1] == [path[-1], nextdir]:
            #count += 1
            #if count >= (len(grid)/5): #yg ini bisa diubah kalo lebih kecil makin dilimit
                #return True
        print(output)
        executedOnce=True
    if(len(output)>0):
        return output.pop(0)
    else:
        return None
    
    