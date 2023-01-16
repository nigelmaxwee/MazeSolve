import math, time, random, os, sys
import matplotlib.pyplot as plt

#Finding length of side of maze
with open("maze.txt", "r") as file:
    big_array = [] 
    for line in file:
        if eval(line):
            big_array.append("wall")
        else:
            big_array.append("space")
total_area = len(big_array) 
length_side = int(math.sqrt(total_area))

#Slicing big array into row arrays
combined_row_array = [] 
for x in range(0, total_area, length_side): 
    array_by_row = big_array[x:(x+length_side)] #individual row
    combined_row_array.append(array_by_row) #combining the individual row with the rest

#Transposition of 2D array
tcombined_row_array = [[combined_row_array[y][x] for y in range(len(combined_row_array))] for x in range(len(combined_row_array[0]))]

#Setting start and end positions
def start_end(position, identifier):
    #function that ask for both starting and end position's row number and column number
    #which are y and x-coordinates respectively
    while True:
        try:
            print("What is the position of the", position, "in this", length_side, "by", length_side, "maze?")
            print("Input values between 1 to 51. Default end point is row 48, column 2.")
            y = int(input("Row number: ")) - 1
            x = int(input("Column number: ")) - 1
            if x<0 or y<0: #value input is negative
                print("Please input valid number")
                continue
        except: #invalid input
            print("Please input valid number.") 
            continue
        try:
            if tcombined_row_array[y][x] == "wall": 
                print(position, "cannot be placed inside a wall, please try a different position.")
                continue
            elif tcombined_row_array[y][x] == "start":
                #prevents end point from replacing the start point
                print(position, "cannot be placed at the start point, please try a different position.")
                continue
            else:
                tcombined_row_array[y][x] = identifier
                if identifier == "start": 
                    #getting the starting x and y-coordinates
                    global start_x
                    start_x = x
                    global start_y
                    start_y = y
                break
        except: #outside of maze
            print("Please input valid number.") 
            continue

start_x = 0 
start_y = 0 
start_end("Starting point", "start") #function to get starting position
start_end("Red dot", "end") #function to get end position/red dot


#Converting maze into 2D list and plotting out   
def display_maze(maze_new, path):
    os.system('cls') #clears the console
    for item in path: #iterate through the path tuple
        maze_new[item[0]][item[1]] = "path" #sets every square on the path as path
    maze_new[path[-1][0]][path[-1][1]] = "current_position" #sets the very last square as current position
    
    maze = [] #creates empty maze list
    for row in maze_new:
        line = [] #empties the line list at the start of every row iteration 
        for element in row:
            if element == "wall":
                line.append(0)
            if element == "space":
                line.append(1)
            if element == "start":
                line.append(2)
            if element == "end":
                line.append(3)
            if element == "path":
                line.append(4)
            if element == "current_position":
                line.append(5)
            if element == "explored":
                line.append(1)
        maze.append(line) #appends the line list into the maze list
    plt.pcolormesh(maze) #sets plot as a coloured mesh of the 2d-array of numbers that was set above
    plt.xticks([])  #removes the x-axis tick marks
    plt.yticks([])  #removes the y-axis tick marks
    plt.gca().invert_yaxis() #inverts horizontally so that the origin is at the top left instead of bottom left
    plt.show() #displays the coloured mesh and respective settings

#Solving maze using recursion 
def move(path):
    time.sleep(0.005)
    cur = path[-1] #takes most recent position which will be the current position
    display_maze(tcombined_row_array, path) #displays maze with the path argument
    #right, left, down, up from current position
    possibles = [(cur[0],cur[1]+1), (cur[0],cur[1]-1), (cur[0]+1,cur[1]), (cur[0]-1,cur[1])]
    random.shuffle(possibles) #randomises the order of the list
    
    #Exploring possibles
    #The priority is to explore empty squares first
    #If no empty square, backtrack from the path it came from
    for item in possibles:
        if tcombined_row_array[item[0]][item[1]] in ["wall", "explored"]:  
            #if next position is a wall or explored, ignore
            continue
        elif item in path: 
            #if next position is in the path, ignore
            continue
        elif tcombined_row_array[item[0]][item[1]] == "end": 
            #if next position is end point, end function
            path = path + (item,)
            display_maze(tcombined_row_array, path)
            input("Solution found! Press enter to finish")
            os.system('cls')
            sys.exit()
        else:
            #if next position is space, continue exploring down the recursion tree
            #if no space, go back up the recursion tree
            #displays the previous path not the newpath
            #this shows the backtracking of the current position
            newpath = path + (item,) 
            move(newpath)
            tcombined_row_array[item[0]][item[1]] = "explored" #mark backtracked path so that do not explore into this explored path.
            display_maze(tcombined_row_array, path)
            time.sleep(0.005)

#starts by letting the current position be the starting position
move(((start_y,start_x),)) 
