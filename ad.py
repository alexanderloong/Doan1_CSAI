from tkinter import *
import tkinter as ttk
from tkinter import filedialog
from tkinter import messagebox
from time import sleep
import sys
from math import sqrt

HEIGHT_MATRIX =600
WIDTH_MATRIX = 1000

#SIZE_WALL_REC = 20


class Node:                                                             # Class Node
    index =[]
    gScore = 0
    fScore = 0
    cameFrom = None
    
def read_and_create_map(input,tk):
    
    file_input = open(input, mode = 'r')  # Hàm đọc file    
    global map_size, start, goal, map_game
    map_size, start, goal, map_game = [], [], [], []
    while True:
        data = file_input.readline()
        if map_size == []:
            data = list(data.split(' '))
            map_size = [int(data[0]), int(data[1])]
            #print(map_size)
            continue
        
        if start == []:
            data = list(data.split(' '))
            start = [int(data[0]), int(data[1])]
            continue
        if goal == []:
            data = list(data.split(' '))
            goal = [int(data[0]), int(data[1])]
            break
    for k in range(map_size[0]):
        mapsample = []
        data = file_input.readline().split()
        for i in range(map_size[1]):
            mapsample.append(int(data[i]))
        map_game.append(mapsample)
    #print(map_game)
    global SIZE_WALL_REC

    if (map_size[0] >= 50 or map_size[1] >=50):
        SIZE_WALL_REC = 800/max(map_size)
    elif (map_size[0] > 30 or map_size[1] >30) :
        SIZE_WALL_REC = 25
    elif (map_size[0] > 15 or map_size[1] > 15) :
        SIZE_WALL_REC = 30
    else:
        SIZE_WALL_REC = 50
    if (map_game[goal[0]][goal[1]] == 1):
        map_game[goal[0]][goal[1]] = 0
    if (map_game[start[0]][start[1]] == 1):
        map_game[start[0]][start[1]] = 0
    



def mahattan(curindex, goindex):                                        # Hàm tính khoảng cách Mahattan cho Heuristic
    h = abs(curindex[0] - goindex[0]) + abs(curindex[1] - goindex[1])
    return h

def euclid(curindex, goindex):    
    h = sqrt((goindex[0]-curindex[0])**2 + (goindex[1]-curindex[1])**2 )
    return h  # Hàm tính khoảng cách Euclid cho Heuristic

def lowest_fscore(openset):                                             # Tìm node có fScore nhỏ nhất trong list openSet
    indeX = 0
    k = None
    for i in range(len(openset)):
        if k == None:
            k = openset[i].fScore
        else:
            if openset[i].fScore < k:
                k = openset[i].fScore
                indeX = i
    return indeX


def reconstruct_path(current):                                          # Trả về index đường đi ngắn nhất
    total_path = [current.index]
    while current.cameFrom != None:
        current = current.cameFrom
        total_path.append(current.index)

    total_path.reverse()
    return total_path

def neighbor(current,ca,map_game,start,goal):                                                  # Trả về list index hàng xóm của node đang xét
    indexcur = current.index

    N = [indexcur[0] - 1, indexcur[1]]
    S = [indexcur[0] + 1, indexcur[1]]
    E = [indexcur[0], indexcur[1] + 1]
    W = [indexcur[0], indexcur[1] - 1]
    NE = [indexcur[0] - 1, indexcur[1] + 1]
    NW = [indexcur[0] - 1, indexcur[1] - 1]
    SE = [indexcur[0] + 1, indexcur[1] + 1]
    SW = [indexcur[0] + 1, indexcur[1] - 1]

    nb = [N, S, E, W, NE, NW, SE, SW]
    i = 0

    while i < len(nb) :
        if nb[i][0] == -1 or nb[i][0] > map_size[0] - 1:
            nb.pop(i)
            continue
        if nb[i][1] == -1 or nb[i][1] > map_size[1] - 1:
            nb.pop(i)
            continue
        if map_game[nb[i][0]][nb[i][1]] == 1:
            nb.pop(i)
            continue
        i += 1 

    i = 0
    while i < len(nb) :
        if nb[i] == NE:
            if (N  not in nb) and (E  not in nb):
                nb.pop(i)
                continue
        if nb[i] == NW:
            if (N  not in nb) and (W  not in nb):
                nb.pop(i)
                continue
        if nb[i] == SE:
            if (S  not in nb) and (E  not in nb):
                nb.pop(i)
                continue
        if nb[i] == SW:
            if (S  not in nb) and (W  not in nb):
                nb.pop(i)
                continue
        i += 1
    


    
    something = nb
    for j in something:
        #print(nb)
        #sleep(0.1)
        #print(j[0],j[1])
        if(map_game[j[0]][j[1]] != 1):
            # print(j[0],j[1])
            #print(goal,start)
            if (j[0] == start.index[0] and j[1] == start.index[1]):
                continue
            elif (j[0] == goal.index[0] and j[1] == goal.index[1]):
                continue
            else:
            #ca.create_rectangle(SIZE_WALL_REC*start.index[1],SIZE_WALL_REC*start.index[0],SIZE_WALL_REC*start.index[1]+SIZE_WALL_REC,SIZE_WALL_REC*start.index[0]+SIZE_WALL_REC,fill = "red",outline = "white",width = 1)
                ca.create_rectangle(SIZE_WALL_REC*(j[1]),SIZE_WALL_REC*(j[0]),SIZE_WALL_REC*(j[1])+SIZE_WALL_REC,SIZE_WALL_REC*(j[0])+SIZE_WALL_REC,fill = "SkyBlue4",outline = "white",width = 1)
                ca.update()
            #print("Rectangle Create !!!!!!!!!!!!!!!!!!!!!!")

    node_nb = []
    for i in nb:
        nnbb = Node()
        nnbb.index = i

        node_nb.append(nnbb)

    return node_nb


def a_star(S, G,ca,map_game,start,goal):                                                       # Thuật toán A*
    start = Node()
    goal = Node()

    start.index = S
    goal.index = G

    start.fScore = euclid(S, G)

    openSet = [start]
    closeSet = []

    while len(openSet) != 0:                                            # Trong khi list openSet khác rỗng, xét phần tử có fScore nhỏ nhất
        current = Node()                        
        index_lowest = lowest_fscore(openSet)   
        current = openSet[index_lowest]

        closeSet.append(openSet[index_lowest].index)                    # Đưa vào closeSet
        openSet.pop(index_lowest)                                       # Sau đó xoá trong openSet
        

        if current.index == goal.index:                                 # Trả về đường đi nếu Node đang xét là goal
            return reconstruct_path(current)
        
        for  nb in neighbor(current,ca,map_game,start,goal):                                   # Xét từng hàng xóm của current
            if nb.index in closeSet:                                    # Nếu có trong Close Set thì không xét
                continue

            for i in openSet:
                if nb.index == i.index:
                    nb = i

            d = euclid(current.index, nb.index)                       # Khoảng cách Euclid của Current đến hàng xóm
            tentative_gScore = current.gScore + d                       # tentative_gScore = Start -> Current + Current -> Hàng xóm

            if tentative_gScore < nb.gScore or nb.gScore == 0:         # Nếu tentative_gScore nhỏ hơn gScore của hàng xóm đang có
                nb.cameFrom = Node()                                   # hoặc gScore của hàng xóm = không thì xử lý chúng
                nb.cameFrom = current
                nb.gScore = tentative_gScore
                nb.fScore = nb.gScore + euclid(nb.index, goal.index)
                if nb not in openSet:                                  # Add vào openSet nếu chưa tồn tại trong openSet
                    openSet.append(nb)


    return -1

        
def Create_Matrix(tk, map_size,start , goal, map_game):
    
    #print(map_size[1]*SIZE_WALL_REC)
    #print(map_size[0]*SIZE_WALL_REC)
    #print(map_size)
    for i in range(0,map_size[1]+1):                                                    #Ve duong doc
        ca.create_line(SIZE_WALL_REC*i,0,SIZE_WALL_REC*i,map_size[0]*SIZE_WALL_REC, fill= "white")
    for i in range(0,map_size[0]+1):                                                    #Ve duong ngang
        ca.create_line(0,SIZE_WALL_REC*i,map_size[1]*SIZE_WALL_REC,SIZE_WALL_REC*i, fill= "white")
    #for i in range (0,map_size[1]):
        #sleep(0.1)
        #ca.create_rectangle(SIZE_WALL_REC*i,SIZE_WALL_REC*i,SIZE_WALL_REC*i+SIZE_WALL_REC,SIZE_WALL_REC*i+SIZE_WALL_REC,fill = "SkyBlue1",outline = "white",width = 1)
        #ca.update()

    for i in range(0,map_size[1]):
        for j in range(0,map_size[0]):
            if (map_game[j][i] == 1):
                ca.create_rectangle(SIZE_WALL_REC*i,SIZE_WALL_REC*j,SIZE_WALL_REC*i+SIZE_WALL_REC,SIZE_WALL_REC*j+SIZE_WALL_REC,fill = "black",outline = "white",width = 1) 
    ca.create_rectangle(SIZE_WALL_REC*start[1],SIZE_WALL_REC*start[0],SIZE_WALL_REC*start[1]+SIZE_WALL_REC,SIZE_WALL_REC*start[0]+SIZE_WALL_REC,fill = "magenta2",outline = "white",width = 1) # Ve diem Start
    ca.create_rectangle(SIZE_WALL_REC*goal[1],SIZE_WALL_REC*goal[0],SIZE_WALL_REC*goal[1]+SIZE_WALL_REC,SIZE_WALL_REC*goal[0]+SIZE_WALL_REC,fill = "red",outline = "white",width = 1)   #Ve diem Goal           
    ca.configure(scrollregion=ca.bbox("all"))
    #print(start)
    #print(goal)
    
    global Click_Start2
    Click_Start2=  Button(tk,text="RUN", command = Clickme2,fg="black",bg="white").place(x=700, y=10)
   # Click_Start2.pack(side=TOP)
    

def Start_Finding(S,G,ca,map_game,start,goal):
    final_result = a_star(start,goal,ca,map_game,start,goal)
    if final_result == -1:
        print("Khong co duong")
        messagebox.showinfo("Thông Báo","Không có đường đi đến điểm Goal")
    else:
        for i in final_result:
            if (i[0] == start[0] and i[1] == start[1]):
                continue
            elif (i[0] == goal[0] and i[1] == goal[1]):
                continue
            else:
                #ca.create_rectangle(SIZE_WALL_REC*start[1],SIZE_WALL_REC*start[0],SIZE_WALL_REC*start[1]+SIZE_WALL_REC,SIZE_WALL_REC*start[0]+SIZE_WALL_REC,fill = "red",outline = "white",width = 1)
                sleep(0.05)
                
                ca.create_rectangle(SIZE_WALL_REC*i[1],SIZE_WALL_REC*i[0],SIZE_WALL_REC*i[1]+SIZE_WALL_REC,SIZE_WALL_REC*i[0]+SIZE_WALL_REC,fill = "yellow",outline = "yellow",width = 0)
                #ca.create_rectangle(SIZE_WALL_REC*goal[1],SIZE_WALL_REC*goal[0],SIZE_WALL_REC*goal[1]+SIZE_WALL_REC,SIZE_WALL_REC*goal[0]+SIZE_WALL_REC,fill = "red",outline = "white",width = 1)
                ca.update()

def Openfile():
    #read_and_create_map("input.txt",tk)
    global filename,ca,scrollbar,scrollbar_2
    filename = filedialog.askopenfilename()
    scrollbar = Scrollbar(tk,orient=VERTICAL)
    scrollbar.pack( side = RIGHT, fill = Y )
    scrollbar_2 = Scrollbar(tk,orient=HORIZONTAL)
    scrollbar_2.pack(side = BOTTOM,  fill = BOTH)
    read_and_create_map(filename,tk)
    ca= Canvas(tk, width = map_size[1]*SIZE_WALL_REC, height = map_size[0]*SIZE_WALL_REC , bg = "LightBlue1",yscrollcommand = scrollbar.set,xscrollcommand = scrollbar_2.set)
    ca.pack(side = BOTTOM)
    ca.delete("all")
    Create_Matrix(tk, map_size, start, goal,map_game)
    scrollbar.config( command = ca.yview )
    scrollbar_2.config( command = ca.xview )
def Clickme2():
    Start_Finding(start,goal,ca,map_game,start,goal)
def ClearClick():
    ca.destroy()
    scrollbar.destroy()
    scrollbar_2.destroy()
    #Click_Start2.destroy()
    
    

    
tk = Tk()
tk.geometry("1200x700")
tk.title("Huy Pro 3.0")


my_menu = Menu(tk)
tk.config(menu=my_menu)
open_menu = Menu(my_menu)
my_menu.add_cascade(label = "File",menu = open_menu )
open_menu.add_command(label = "Open File", command = Openfile)
open_menu.add_separator()
open_menu.add_command(label = "Clear File", command = ClearClick)


#Click_Start =  Button(tk,text="OPEN FILE", command = Openfile,fg="black",bg="white").place(x=10, y=50)

#Click_Clear =  Button(tk,text="CLEAR", command = ClearClick,fg="black",bg="white").place(x=10, y=100)
    


    #read_and_create_map("input.txt",tk)

tk.mainloop()
    

