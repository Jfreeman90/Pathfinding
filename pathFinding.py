import tkinter as tk
from tkinter import messagebox

#main path finding algorpthm
def find_best_diagonal_path(start, end, matrix):
    from pathfinding.core.grid import Grid
    from pathfinding.finder.a_star import AStarFinder
    from pathfinding.core.diagonal_movement import DiagonalMovement
    #create the grid 
    grid=Grid(matrix=matrix)
    
    #create starting and end points (columns, row)
    start=grid.node(start[0], start[1])
    end=grid.node(end[0], end[1])
    #find the path
    finder=AStarFinder(diagonal_movement = DiagonalMovement.always)

    #runs is the amount of iterations needed to find the shortest distance
    path, runs=finder.find_path(start,end, grid)
    distance=len(path)-2
    #print('\nOptimal path with diagonal', path)
    #print('Runs', runs)
    #print('Distance(sqaures entered)', distance)
    return path

#main path finding algorithm without diagonally going past obstacles
def find_best_path(start, end, matrix):
    from pathfinding.core.grid import Grid
    from pathfinding.finder.a_star import AStarFinder
    #create the grid 
    grid=Grid(matrix=matrix)
    
    #create starting and end points (columns, row)
    start=grid.node(start[0], start[1])
    end=grid.node(end[0], end[1])
    #find the path
    finder=AStarFinder()

    #runs is the amount of iterations needed to find the shortest distance
    path, runs=finder.find_path(start,end, grid)
    distance=len(path)-2
    #print('\nOptimal path with diagonal', path)
    #print('Runs', runs)
    #print('Distance(sqaures entered)', distance)
    return path


#draw out the starting grid
def draw_grid():
    #create the grid outline for the canvas that will always be there, as a background
    for i in range(grid_size+1):
        #draw the blue outlines every 3rd across
        color='grey'
        width=1
        
        #vertical lines
        xv0=MARGIN + (i*cell_width)
        yv0=MARGIN
        xv1=MARGIN + (i*cell_width)
        yv1=WIN_HEIGHT  - MARGIN
        main_canvas.create_line(xv0, yv0, xv1, yv1, fill=color, width=width)
        
        #horizontal lines
        xh0= MARGIN
        yh0= MARGIN + (i*cell_width)
        xh1= WIN_WIDTH - MARGIN
        yh1 = MARGIN + (i*cell_width)
        main_canvas.create_line(xh0, yh0, xh1, yh1, fill=color, width=width)

#function that confirms the placement on the grid so that it cant be edited or clicked to change values after
def confirm_drawing():
    global start_point, end_point, obstacles_on
    #start_point=0
    #end_point=0
    
#highlight and change the variables of the grid clicked 
def cell_right_clicked(event):
    from math import floor
    #main_canvas.delete("cursor highlight")
    x,y=event.x, event.y

#remove variables or clear cell if needed
def cell_clicked(event):
    from math import floor
    #main_canvas.delete("cursor highlight")
    x,y=event.x, event.y
    #print(x,y)
    #check that the location clicked is on the board
    global start_point, end_point, obstacles_on, starting_point, ending_point
    if start_point==1:
        if MARGIN < x < WIN_WIDTH - MARGIN and MARGIN < y < WIN_HEIGHT - MARGIN:
            #get row and column index from position
            global row, col, x0, y0, x1, y1
            row, col = floor((y - MARGIN) / cell_width), floor((x - MARGIN) / cell_width)
            #print(row, col)
            x0 = MARGIN + col * cell_width + 1
            y0 = MARGIN + row * cell_width + 1
            x1 = MARGIN + (col + 1) * cell_width - 1
            y1 = MARGIN + (row + 1) * cell_width - 1
            main_canvas.delete('start_')
            #create the starting point grid vvariable that can be fed into the path finder
            starting_point=(col,row)
            main_canvas.create_rectangle(x0, y0, x1, y1, fill="#8FBC8B", width=1, tags="start_")
        start_point=0
        lbl_info['text']='Starting Point: '+str(starting_point)
        
    #create a different point and drawing if the suer has decided to create an end point.
    elif end_point==1:
        if MARGIN < x < WIN_WIDTH - MARGIN and MARGIN < y < WIN_HEIGHT - MARGIN:
            #get row and column index from position
            row, col = floor((y - MARGIN) / cell_width), floor((x - MARGIN) / cell_width)
            #print(row, col)
            x0 = MARGIN + col * cell_width + 1
            y0 = MARGIN + row * cell_width + 1
            x1 = MARGIN + (col + 1) * cell_width - 1
            y1 = MARGIN + (row + 1) * cell_width - 1
            #create the starting point grid vvariable that can be fed into the path finder
            main_canvas.delete('end')
            ending_point=(col,row)
            main_canvas.create_rectangle(x0, y0, x1, y1, fill="#DC143C", width=1, tags="end_")
        end_point=0
        lbl_info['text']='Starting Point: '+str(starting_point) + '   End Point: ' +str(ending_point)

    #create and edit the starting point with 0's where obstacles are drawn
    elif obstacles_on==1:
        if MARGIN < x < WIN_WIDTH - MARGIN and MARGIN < y < WIN_HEIGHT - MARGIN:
            #get row and column index from position
            row, col = floor((y - MARGIN) / cell_width), floor((x - MARGIN) / cell_width)
            #print(row, col)
            x0 = MARGIN + col * cell_width + 1
            y0 = MARGIN + row * cell_width + 1
            x1 = MARGIN + (col + 1) * cell_width - 1
            y1 = MARGIN + (row + 1) * cell_width - 1
            global starting_grid
            #changle the starting grid values to 0 where the obstacles are drawn
            starting_grid[row][col]=0
            main_canvas.create_rectangle(x0, y0, x1, y1, fill="black", tags="obstacles_")
        start_point=0
        end_point=0
    else:
        pass
   
    
#from the cell_clicked set the correct variables for the starting position
def get_start_point():
    #create a variable to allow the checks to know start_point has been pressed
    global start_point
    start_point=1


#from the cell_clicked set the correct variables for the ending position
def get_end_point():
    #create a variable to allow the checks to know end_point has been pressed
    global end_point
    end_point=1

#allow the user to click on the grid and draw in obsacles that can block the path between two points
def draw_obstacles():
    #create a variable to allow the checks to know obstacles has been pressed
    global obstacles_on
    obstacles_on=1
  
#find the path and draw it on  
def find_diag_path():
    from time import sleep
    global starting_grid, starting_point, ending_point
    #print(starting_grid)
    #print('START:',starting_point)
    #print('END:', ending_point)
    best_path=find_best_diagonal_path(starting_point, ending_point, starting_grid)
    #each grid co-ordinate to draw without start and end included as to not draw over them
    draw_path=best_path[1:-1]
    #print(draw_path)
    for square in draw_path:
        col=square[0]
        row=square[1]
        x0 = MARGIN + col * cell_width + 1
        y0 = MARGIN + row * cell_width + 1
        x1 = MARGIN + (col + 1) * cell_width - 1
        y1 = MARGIN + (row + 1) * cell_width - 1
        main_canvas.create_rectangle(x0, y0, x1, y1, fill="#FFA07A", width=1, tags="path_")
        sleep(0.5)
        main_canvas.update()

#find the path and draw it on  
def find_path():
    from time import sleep
    global starting_grid, starting_point, ending_point
    #print(starting_grid)
    #print('START:',starting_point)
    #print('END:', ending_point)
    best_path=find_best_path(starting_point, ending_point, starting_grid)
    #each grid co-ordinate to draw without start and end included as to not draw over them
    draw_path=best_path[1:-1]
    #print(draw_path)
    for square in draw_path:
        col=square[0]
        row=square[1]
        x0 = MARGIN + col * cell_width + 1
        y0 = MARGIN + row * cell_width + 1
        x1 = MARGIN + (col + 1) * cell_width - 1
        y1 = MARGIN + (row + 1) * cell_width - 1
        main_canvas.create_rectangle(x0, y0, x1, y1, fill="#FF7F50", width=1, tags="path_")
        sleep(0.5)
        main_canvas.update()
        
#reset the grid and drawing and path finding algorithms to try again with a different user input
def reset_drawing():
    global starting_grid, grid_size
    main_canvas.delete('start_')
    main_canvas.delete('end_')
    main_canvas.delete('obstacles_')
    main_canvas.delete('path_')
    from numpy import ones
    starting_grid=ones((grid_size, grid_size))
    
#global variables and different sizes of the grid and cells
global WIN_HEIGHT, WIN_WIDTH, MARGIN, cell_width, grid_size, starting_grid, start_point, end_point, obstacles_on
MARGIN=40
cell_width=15
grid_size=30
WIN_HEIGHT=MARGIN * 2 + cell_width * grid_size
WIN_WIDTH=MARGIN * 2 + cell_width * grid_size
#initiate a starting grid that can be represented by the grid
from numpy import ones
starting_grid=ones((grid_size, grid_size))
start_point=0
end_point=0
obstacles_on=0


#ALL OF THE BELOW IS FORMATING FOR THE GUI AND ITS DISPLAYS
# Create instance
window = tk.Tk()
# Disable resizing the GUI
window.resizable(0,0)  #(x,y)
# Add a title
window.title("Path Finding - APP (jlf)")

#frame to hold the title infomation
frm_title=tk.Frame(master=window, bg='black')
frm_title.grid(row=0, column=0, sticky="ew")
frm_title.grid_columnconfigure([0,1], weight=1)

#LABEL - Choose the words difficulty
lbl_title=tk.Label(master=frm_title, 
                text="Path Finding", font=("Minion Pro Med", 20,  "bold italic"), fg="white", bg="black")
lbl_title.grid(row=0, column=0, columnspan=2, sticky='ew')

lbl_info=tk.Label(master=frm_title, 
                text=" ", font=("Minion Pro Med", 14,  "bold italic"), fg="white", bg="black")
lbl_info.grid(row=1, column=0, sticky='ew')

#button to confirm_drawing
confirm_btn=tk.Button(master=frm_title, text='Confirm positions', command=get_end_point)
confirm_btn.grid(row=1, column=1, sticky='e', padx=(0,10), pady=(0,5))

#frame to fill in the blank space
frm_title_space=tk.Frame(master=window, bg='black')
frm_title_space.grid(row=0, column=1, sticky="ew")
lbl_title_empty=tk.Label(master=frm_title_space,  text=" ",font=("Minion Pro Med", 16,  "bold italic"),fg='white', bg="black")
lbl_title_empty.grid(row=0, column=0, sticky='nsew')
lbl_title_empty2=tk.Label(master=frm_title_space,  text=" ", font=("Minion Pro Med", 18, "bold italic"),fg='white',bg="black")
lbl_title_empty2.grid(row=1, column=0, sticky='nsew', pady=(0,5))

#frame to hold the main canvas and buttons
frm_main_buttons=tk.Frame(master=window, bg='black')
frm_main_buttons.grid(row=1, column=1, sticky="nsew")
frm_main_buttons.grid_rowconfigure([0,1,2,3,4,5], weight=1)
frm_main_buttons.grid_columnconfigure(0, weight=1)

#get the starting point co-ordinate
start_point_btn=tk.Button(master=frm_main_buttons, text='Get Start', width = 14, bg="#8FBC8B", command=get_start_point)
start_point_btn.grid(row=0, column=0,padx=(5,5))

#get the ending point co-ordinate
end_point_btn=tk.Button(master=frm_main_buttons, text='Get End', bg="#DC143C",width = 14, command=get_end_point)
end_point_btn.grid(row=1, column=0,padx=(5,5))

#get the ending point co-ordinate
obstacles_btn=tk.Button(master=frm_main_buttons, text='Draw obstacles', width = 14,command=draw_obstacles)
obstacles_btn.grid(row=2, column=0,padx=(5,5))

#Find the best path between the two co-ordinates
find_diag_path_btn=tk.Button(master=frm_main_buttons, text='Find Path Diag', bg="#FFA07A",width = 14, command=find_diag_path)
find_diag_path_btn.grid(row=3, column=0,padx=(5,5))

#Find the best path between the two co-ordinates
find_path_btn=tk.Button(master=frm_main_buttons, text='Find Path', bg="#FF7F50",width = 14, command=find_path)
find_path_btn.grid(row=4, column=0,padx=(5,5))

#Find the best path between the two co-ordinates
reset_btn=tk.Button(master=frm_main_buttons, text='Reset drawing', width = 14,command=reset_drawing)
reset_btn.grid(row=5, column=0,padx=(5,5))

#frame to hold the main canvas
frm_main_canvas=tk.Frame(master=window, bg='black')
frm_main_canvas.grid(row=1, column=0, sticky="ew")

#canvas where the board will be drawn
main_canvas=tk.Canvas(master=frm_main_canvas, width=WIN_WIDTH, height=WIN_HEIGHT, bg='white')
main_canvas.grid(row=0, column=0)
main_canvas.bind("<Button-1>", cell_clicked)   #bind left mouse click to the canvas with a command to follow
main_canvas.bind("<Button-3>", cell_right_clicked)   #bind left mouse click to the canvas with a command to follow

#draw the grid
draw_grid()

# Run the application
window.mainloop()