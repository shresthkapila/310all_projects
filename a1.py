# a1.py

import sys
import random
import time
sys.path.insert(0, 'C:\\Users\\mahkh\\aima-python')

from search import *

# ...code Assignment 1 ------------------------------------------------------------------------------------------------------------

""" 
Sources (Major help from) :
         W3Schools, https://docs.python.org/3/ 
"""


#-----------------------------------------------------------------------------------------------------------------------------------
# Question 2
def Astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return updated_best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def ManhattanDistance(self,node):
        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhd1 = 0
        mhd2 = 0

        for i in range(8):
            mhd1 = abs(index_goal[i][0] - index_state[i][0]) + mhd1
            mhd2 = abs(index_goal[i][1] - index_state[i][1]) + mhd2

        return mhd1+mhd2
        
    def MaxDistance(self,node):
        return max(self.h(node), self.ManhattanDistance(node)) 
    
#-------------------------------------------------------------------------------------------------------------------------
# Question 1
def make_rand_EightPuzzle():

    size = 9
    rand_puzzle = [size] * size
    for x in range(size):
        rand_tile = random.randint(0,8)
        while rand_tile in rand_puzzle:
            rand_tile = random.randint(0,8)
        rand_puzzle[x] = rand_tile

    puzzle_tuple = tuple(rand_puzzle)
    rand_8puzzle = EightPuzzle(puzzle_tuple)
    
    while (rand_8puzzle.check_solvability(rand_8puzzle.initial) != True):
        size = 9
        rand_puzzle = [size] * size
        for x in range(size):
            rand_tile = random.randint(0,8)
            while rand_tile in rand_puzzle:
                rand_tile = random.randint(0,8)
            rand_puzzle[x] = rand_tile

        puzzle_tuple = tuple(rand_puzzle)
        rand_8puzzle = EightPuzzle(puzzle_tuple) 

    return rand_8puzzle

# Question 1
def display_EightPuzzle(state):
    state_array = list(state)

    empty_tile = state_array.index(0)
    state_array[empty_tile] = '*'

    print ("****************")
    print ("| Eight Puzzle |")
    print ("****************")
    print (state_array[0], state_array[1], state_array[2])
    print (state_array[3], state_array[4], state_array[5])
    print (state_array[6], state_array[7], state_array[8])
    print ("    ")

#-----------------------------------------------------------------------------------------------------------------------
# Question 2
def updated_best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    countRemove = 0
    while frontier:
        node = frontier.pop()
        countRemove += 1
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return [node, countRemove]
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


for x in range(10):
    puzzle = make_rand_EightPuzzle()
    display_EightPuzzle(puzzle.initial)

    # Misplaced tile heuristic 
    print("***********************************************")
    print("| A*search using the misplaced tile heuristic |")
    print("***********************************************")
    start_time = time.time()
    search_1 = Astar_search(puzzle)
    elapsed_time = time.time() - start_time
    print(f'==> total time (in seconds): {elapsed_time}')
    print(f'==> number of tiles moved: {search_1[0].path_cost} ')
    print(f'==> total number of nodes removed from frontier: {search_1[1]} \n')

    # Manhattan distance heuristic 
    print("***************************************************")
    print("| A*search using the Manhattan distance heuristic |")
    print("***************************************************")
    start_time = time.time()
    search_2 = Astar_search(puzzle,puzzle.ManhattanDistance)
    elapsed_time = time.time() - start_time
    print(f'==> total time (in seconds): {elapsed_time}')
    print(f'==> number of tiles moved: {search_2[0].path_cost} ')
    print(f'==> total number of nodes removed from frontier: {search_2[1]} \n')

    # Maximum distance heuristic 
    print("*************************************************************************************")
    print("| A*search using the maximum of the Misplaced tile and Manhattan distance heuristic |")
    print("*************************************************************************************")
    start_time = time.time()
    search_3 = Astar_search(puzzle,puzzle.MaxDistance)
    elapsed_time = time.time() - start_time
    print(f'==> total time (in seconds): {elapsed_time}')
    print(f'==> number of tiles moved: {search_3[0].path_cost} ')
    print(f'==> total number of nodes removed from frontier: {search_3[1]} \n')

    print (f'--------------------------------------------------------------end')

#------------------------------------------------------------------------------------------------------------------------------
# END OF EIGHT PUZZLE

#------------------------------------------------------------------------------------------------------------------------------

# Question 3
class DuckPuzzle(Problem):

    def __init__(self, initial, goal = (1,2,3,4,5,6,7,8,0)):
        super().__init__(initial,goal)
    
    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        leftNotAllowed = (0,2,6)
        upNotAllowed = (0,1,4,5)
        rightNotAllowed = (1,5,8)
        downNotAllowed = (2,6,7,8)
        
        if index_blank_square in leftNotAllowed:
            possible_actions.remove('LEFT')
        if index_blank_square in upNotAllowed:
            possible_actions.remove('UP')
        if index_blank_square in rightNotAllowed:
            possible_actions.remove('RIGHT')
        if index_blank_square in downNotAllowed:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        blank_2move = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        blank_2 = (1,2,0)
        blank_23move = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        blank_23 = (3,)
        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        
        if blank in blank_2:
            neighbor = blank + blank_2move[action]
        elif blank in blank_23:
            neighbor = blank + blank_23move[action]
        else:
            neighbor = blank + delta[action]
        
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def h(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def ManhattanDistance(self, node):
        state = node.state
        index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
        index_state = {}
        index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

        for i in range(len(state)):
            index_state[state[i]] = index[i]

        mhd1 = 0
        mhd2 = 0

        for i in range(8):
            mhd1 = abs(index_goal[i][0] - index_state[i][0]) + mhd1
            mhd2 = abs(index_goal[i][1] - index_state[i][1]) + mhd2

        return mhd1+mhd2
    
    def MaxDistance(self, node):
        return max(self.h(node), self.ManhattanDistance(node))


def make_rand_duckPuzzle():
    size = 9
    rand_puzzle = [size] * size

    for i in range(size):
        rand_tile = random.randint(0,8)
        while rand_tile in rand_puzzle:
            rand_tile = random.randint(0,8)
        
        rand_puzzle[i] = rand_tile

    puzzle_tuple = tuple(rand_puzzle)
    rand_duckPuzzle = DuckPuzzle(puzzle_tuple)

    return rand_duckPuzzle


def display_duckPuzzle(state):
    state_array = list(state)

    empty_tile = state_array.index(0)
    state_array[empty_tile] = '*'

    print ("***************")
    print ("| Duck Puzzle |")
    print ("***************")
    print (state_array[0], state_array[1], " ", " ")
    print (state_array[2], state_array[3], state_array[4], state_array[5])
    print (" ", state_array[6], state_array[7], state_array[8])
    print ("    ")


for y in range(10):
    flag = False 
    puzzle_2 = make_rand_duckPuzzle()

    # Misplaced tile heuristic 
    start_time = time.time()
    search_4 = Astar_search(puzzle_2)
    elapsed_time = time.time() - start_time

    while search_4 is None:
        puzzle_2 = make_rand_duckPuzzle()
        start_time2 = time.time()
        search_4 = Astar_search(puzzle_2)
        elapsed_time2 = time.time() - start_time2
        flag = True

    display_duckPuzzle(puzzle_2.initial)

    print("***********************************************")
    print("| A*search using the misplaced tile heuristic |")
    print("***********************************************")
    if flag == True:
        print(f'==> total time (in seconds): {elapsed_time2}')
    else:
        print(f'==> total time (in seconds): {elapsed_time}s')
    print(f'==> number of tiles moved: {search_4[0].path_cost} ')
    print(f'==> total number of nodes removed from frontier: {search_4[1]} \n')

    # Manhattan distance heuristic 
    start_time = time.time()
    search_5 = Astar_search(puzzle_2,puzzle_2.ManhattanDistance)
    elapsed_time = time.time() - start_time

    print("***************************************************")
    print("| A*search using the Manhattan distance heuristic |")
    print("***************************************************")
    print(f'==> total time (in seconds): {elapsed_time}')    
    print(f'==> number of tiles moved: {search_5[0].path_cost} ')
    print(f'==> total number of nodes removed from frontier: {search_5[1]} \n')


    # Maximum distance heuristic 
    start_time = time.time()
    search_6 = Astar_search(puzzle_2,puzzle_2.ManhattanDistance)
    elapsed_time = time.time() - start_time
    
    print("*************************************************************************************")
    print("| A*search using the maximum of the Misplaced tile and Manhattan distance heuristic |")
    print("*************************************************************************************")
    print(f'==> total time (in seconds): {elapsed_time}')
    print(f'==> number of tiles moved: {search_6[0].path_cost} ')
    print(f'==> total number of nodes removed from frontier: {search_6[1]} \n')

    print (f'--------------------------------------------------------------end')



    #-----------------------------------------------------------------------------------------------------------------------------------------------
    # END OF DUCK PUZZLE
    # END OF ASSIGNMENT 1
    #-----------------------------------------------------------------------------------------------------------------------------------------------