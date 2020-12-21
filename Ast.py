import copy
import math
import heapq as hq
curr_state = None
class configuration():

    def __init__(self, fn_cost,array,parent,action_type):
        self.fn_cost = fn_cost
        self.board = array
        self.action_type=action_type
        self.parent=parent

    def __lt__(self, other):
        return self.fn_cost < other.fn_cost

    def get_parent(self):
        return self.parent

def swap(image, i, new_i, j, new_j):
    image[i][j], image[new_i][new_j] = image[new_i][new_j], image[i][j]
    return image

def check_goal(state):
    if (state == goal_state):
        return True
    return False
    return True

def calculate_cost(state, Heuristics_type):
    hn_sum = 0
    if (Heuristics_type == "hattan"):
        for i in range(3):
            for j in range(3):
                current_square = state[i][j]
                h = abs(i - pairs_goal[current_square][0]) + abs(j - pairs_goal[current_square][1])
                hn_sum += h
    else:
        for i in range(3):
            for j in range(3):
                current_square = state[i][j]
                h = math.sqrt(math.sqrt(abs(i - pairs_goal[current_square][0])) + math.sqrt(
                    abs(j - pairs_goal[current_square][1])))
                hn_sum += h

    return (hn_sum + gn)

def generate_neighbours(state, i, j, Heuristics_type):
    # list need to be modified
    list = [copy.deepcopy(state.board), copy.deepcopy(state.board), copy.deepcopy(state.board), copy.deepcopy(state.board)]
    neighbour_list = []

    if (i + 1 < 3):
        state1 = swap(list[0], i, i + 1, j, j)
        neighbour_list.append(configuration(calculate_cost(state1, Heuristics_type), state1, state, "D"))
    if (0 <= i - 1 < 3):
        state2 = swap(list[1], i, i - 1, j, j)
        neighbour_list.append(configuration(calculate_cost(state2, Heuristics_type), state2, state, "U"))
    if (j + 1 < 3):
        state3 = swap(list[2], i, i, j, j + 1)
        neighbour_list.append(configuration(calculate_cost(state3, Heuristics_type), state3, state, "R"))
    if (0 <= j - 1 < 3):
        state4 = swap(list[3], i, i, j, j - 1)
        neighbour_list.append(configuration(calculate_cost(state4, Heuristics_type), state4, state, "L"))
    return neighbour_list

def get_neighbours(state, Heuristics_type):
    x_loop_must_break = False
    neighbours = []
    for i in range(3):
        for j in range(3):
            if (state.board[i][j] == 0):
                x_loop_must_break = True
                break
        if x_loop_must_break:
            break
    neighbours = generate_neighbours(state, i, j, Heuristics_type)
    return neighbours

def in_frontire(state):
    for i in range(len(frontier)):
        if (frontier[i].board == state):
            return True
    return False

def in_explored(state):
    for i in range(len(explored)):
        if (explored[i].board == state):
            return True
    return False

def A_star(initial_state,Heuristics_type):
    global curr_state
    init_state = configuration(0, initial_state, None, None)
    frontier.append(init_state)
    hq.heapify(frontier)
    global gn
    gn = 0
    while frontier:
        hq.heapify(frontier)
        curr_state = hq.heappop(frontier)
        explored.append(curr_state)
        #print("step:", gn)
        #print("current",curr_state.board)
        gn = gn + 1

        # check if is goal
        if check_goal(curr_state.board):
            print("\n * Solved !! *")
            print("*** |path to goal| ****")
            path(curr_state)  # show the path#"""
            return curr_state  #configuration type#
        # loop through neighbours
        neighbours = get_neighbours(curr_state, Heuristics_type)
        for i in range(len(neighbours)):
            if (in_frontire(neighbours[i].board) == False and in_explored(neighbours[i].board) == False):
                frontier.append(neighbours[i])
            else:
                # re-calcuate cost
                continue;

    return None


def path(state):
    if (state == None):
       return
    path(state.parent)
    print(state.action_type)
    print(state.board)


# *** global VARs  *** #
explored = []
frontier = []
# sample trial : [[1,0,2],[7,5,4], [8,6,3]]#
#initial_state = [[1,8,2],[0,4,3], [7,6,5]]
goal_state = [[1,2,3], [4,5,6], [ 7, 8,0]]
pairs_goal = [(2, 2),(0,0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]

"""
# ** Sample Call ** #
Heuristics_type = "Manhattan Distance"  # {"Manhattan Distance","Euclidean Distance"} #
las_visit=A_star(Heuristics_type)  #base Algorithm call#
"""
