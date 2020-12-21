import argparse
import copy
import Ast
import timeit
from collections import deque


# Represents each tile
class Board:
    def __init__(self, parent, array, x, y,direction ,depth ):
        """, new_x, new_y"""
        self.parent = parent
        self.x = x  # X index of  empty tile
        self.y = y  # Y index of  empty tile
        self.array = array
        self.direction = direction
        self.depth = depth

# global variables
N = 3
expandned_nodes  = 0
path=  []
expanded = []  # List to keep track of visited nodes
goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
level =[] #store the level iof each node
cost = 0
key =0 #unique key for each node
MaxSearchDeep = 0
goal_node = None


def printNode(node):
    if node == None:
        return
    for i in range(len(node)):
        for j in range(len(node[i])):
            print(node[i][j], end=" ")
        print(" ")


# valid moves ( up , bottom , left , right )
row = [-1, 1, 0, 0]
col = [0, 0, -1, 1]
# check if (change in x , change in y  ) is valid board corrdinate
def is_safe(x, y):
    if 0 <= x < N and 0 <= y < N:
        return True
    return False


def swap(array, x, new_x, y, new_y):
    new_array = copy.deepcopy(array)
    new_array[x][y], new_array[new_x][new_y] = new_array[new_x][new_y], new_array[x][y]
    return new_array


def is_visited(child):
    for i in range(len(expanded)):
        if child == expanded[i]:
            return True
    return False


def reach_goal(array):
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] != goal[i][j]:
                return False
    return True
def find_path(board, path, flag_printed):
    if board is None:
        return
    find_path(board.parent, path, False)
    path.append(board)
    return path

# retrun the  of direction name
def get_direction(moveX,moveY):
    if moveX ==-1:
        return "up"
    if moveX == 1 :
        return "Down"
    if moveX == 0:
        if moveY == -1:
            return "Left"
        if moveY == 1 :
            return "Right"




def sub_nodes(parent):
    global expandned_nodes,key
    expandned_nodes = expandned_nodes + 1
    sub_nodes = []
    # loop for all possible moves ( neighbours )
    for move in range(4):
        # check if the current move is legal
        if is_safe(parent.x + row[move], parent.y + col[move]):
            new_x = parent.x + row[move]
            new_y = parent.y + col[move]
            # create new child
            child = Board(parent, swap(parent.array, parent.x, new_x, parent.y, new_y), new_x, new_y, get_direction(row[move], col[move]), parent.depth + 1)
            sub_nodes.append(child)
    return sub_nodes

#BFS**************************************************************

def BFS(initial_state, x, y):
    # create root node
    global count
    root = Board(None, initial_state, x, y," ",0)
    #  printNode(root.board)
    # add root to the visited list and the quque\
    frontier = deque([root])

    while frontier:
        s = frontier.popleft()
        expanded.append(s.array)

        # print(count)

        if s.array == goal:
            print("sucess!!!!!!!!!!")
            return s

        # Create list of sub nodes of the current parent
        sub_array = sub_nodes(s)

        for child in sub_array:

            # Check if subnodes[i] is not expanded
            if child.array not in expanded:
                # Add to frontier list
                frontier.append(child)
#DFS**************************************************************

def DFS(initial_state, x, y):
    # create root node
    global count , key, MaxSearchDeep
    root = Board(None, initial_state, x, y," ",0 )
  #  printNode(root.board)
    # add root to the visited list and the quque\
    stack = list([root])

    while stack:
        s = stack.pop()
        expanded.append(s.array)


        if s.array == goal:
            print("sucess!!!!!!!!!!")
            return s

        # Create list of sub nodes of the current parent
        sub_array = sub_nodes(s)
        sub_array.reverse()
        for child in sub_array:

            # Check if subnodes[i] is not expanded
            if child.array not in expanded:
                # Add to stack list
                stack.append( child)
                if child.depth > MaxSearchDeep:
                    MaxSearchDeep = MaxSearchDeep + 1



#conver 1D array to 2Darray
def convert(lst):
    idx = 0
    var_lst = [3, 3, 3]

    for var_len in var_lst:
        yield lst[idx: idx + var_len]
        idx += var_len

def main():
    global path , goal_node

    # Obtain information from calling parameters
    method = input("Enter your search type :#ast bfs dfs# ")
    if method == "ast":
        heuristics = input("Enter heuristics fun :#hattan  Euclidean# ")
    lst1 = [int(item) for item in input("Enter initialBoard :#1,2,3,4,5,6,7,8,0 ").split(',')]
    # Build initial board state
    InitialState = list(convert(lst1))



    for i in range(len(InitialState)):
        for j in range(len(InitialState[i])):
            if (InitialState[i][j] == 0):
                x = i
                y = j
                break

    # Start operation
    start = timeit.default_timer()

    if (method == "bfs"):
        print("BFS >>>>>")
        print(InitialState)
        goal_node = BFS(InitialState, x, y)
    if (method == "dfs"):
        print("DFS >>>>>")
        goal_node = DFS(InitialState, x, y)
    if (method == "ast"):
        print("AST >>>>>")
        goal_node= Ast.A_star(InitialState,heuristics)
        exit(0 )
    stop = timeit.default_timer()
    time = stop - start


    # Print path
    print("Path :")
    path =find_path(goal_node, path, False)

    for node in path:
        printNode(node.array)
        print(node.direction)


    #print
    print()
    print("Path Cost :", len(path))
    print("Running time :", format(time, '.8f'))
    print ("Search Depth ", goal_node.depth)
    print ()
    print ("## Expanded Nodes ## : ", expandned_nodes)
    for node in expanded:
        printNode(node)
        print(",")


if __name__ == '__main__':
    main()
