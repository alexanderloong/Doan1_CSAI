
import sys
from math import sqrt


class Node:                                                             # Class Node
    index =[]
    gScore = 0
    fScore = 0
    cameFrom = None                                                     # Sau này khởi tạo là Node cha

        
def read_data(file_input):                                              # Hàm đọc file    
    global map_size, start, goal, map_game
    map_size, start, goal, map_game = [], [], [], []
    while True:
        data = file_input.readline()
        data = data.split()
        if map_size == []:
            
            map_size = [int(data[0]), int(data[1])]
            continue
        if start == []:
            start = [int(data[0]), int(data[1])]
            continue
        if goal == []:
            goal = [int(data[0]), int(data[1])]
            break

    for k in range(map_size[0]):
        mapsample = []
        data = file_input.readline().split()
        for i in range(map_size[1]):
            mapsample.append(int(data[i]))
        map_game.append(mapsample)
        
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

def neighbor(current):                                                  # Trả về list index hàng xóm của node đang xét
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
        if nb[i][1] == -1 or nb[i][1] > map_size[0] - 1:
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
    


    node_nb = []
    for i in nb:
        nnbb = Node()
        nnbb.index = i

        node_nb.append(nnbb)

    return node_nb


def a_star(S, G):                                                       # Thuật toán A*
    start = Node()
    goal = Node()

    start.index = S
    goal.index = G

    start.fScore = mahattan(S, G)

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
        
        for  nb in neighbor(current):                                   # Xét từng hàng xóm của current
            if nb.index in closeSet:                                    # Nếu có trong Close Set thì không xét
                continue

            for i in openSet:
                if nb.index == i.index:
                    nb = i

            d = mahattan(current.index, nb.index)                       # Khoảng cách Euclid của Current đến hàng xóm
            tentative_gScore = current.gScore + d                       # tentative_gScore = Start -> Current + Current -> Hàng xóm

            if tentative_gScore < nb.gScore or nb.gScore == 0:         # Nếu tentative_gScore nhỏ hơn gScore của hàng xóm đang có
                nb.cameFrom = Node()                                   # hoặc gScore của hàng xóm = không thì xử lý chúng
                nb.cameFrom = current
                nb.gScore = tentative_gScore
                nb.fScore = nb.gScore + mahattan(nb.index, goal.index)
                if nb not in openSet:                                  # Add vào openSet nếu chưa tồn tại trong openSet
                    openSet.append(nb)


    return -1


input = 'input.txt'
output = 'output.txt'

def main(input, output):
    #global map_size, start, goal, map_game
    file_input = open(input, mode = 'r')

    file_output = open(output, mode = 'w')

    read_data(file_input)
    path = a_star(start, goal)

    if path == -1:
        file_output.write('-1')
        return


    for i in path:
        map_game[i[0]][i[1]] = 'x'
    
    map_game[start[0]][start[1]] = 'S'
    map_game[goal[0]][goal[1]] = 'G'

    path_str = ''
    for i in path:
        path_str += str(i)

    file_output.write(path_str + '\n')
    for i in range(map_size[0]):
        map = ''
        for j in range(map_size[1]):
            if map_game[i][j] == 0:
                map += '_ '
            else:
                if map_game[i][j] == 1:
                    map += 'O '
                else:
                    map += map_game[i][j] + ' '
        file_output.write(map + '\n')


    file_input.close()
    file_output.close()




if __name__ == '__main__':
    #main(input, output) 
    main(sys.argv[1], sys.argv[2])              # CMD: tenfile.py fileinput.txt fileoutput.txt