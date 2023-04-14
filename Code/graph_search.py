###### Graph Search ####### 

from asyncio.windows_events import NULL
import sys
import numpy as np
import heapq
import matplotlib.pyplot as plotter
from math import hypot, sqrt
from tilemap import *
# change to be in the form of new game
_ACTIONS = ['u','d','l','r']
_T = 2
_X = 0                                                                          ## 0 is row
_Y = 1                                                                          ## 1 is column
_GOAL_COLOR = 0.75
_INIT_COLOR = 0.25
_PATH_COLOR_RANGE = _GOAL_COLOR-_INIT_COLOR
_VISITED_COLOR = 0.9

def cost(tile):
    if tile.parent is not None:
        if tile.parent in _ACTIONS:
            tile.cost = 1+tile.parent.cost


    return tile

def heur(tile):
    
    yeppers = 2

    return tile + yeppers

def is_goal(goal,s):
    '''
    Test if a specifid state is the goal state

    s - tuple describing the state as (row, col) position on the grid.

    Returns - True if s is the goal. False otherwise.
    '''
    s = list(s)                                                                     ## turns this into a list so the two sides can compare

    return (s[_X] == goal[_X] and
            s[_Y] == goal[_Y])


class SearchTile:
    def __init__(self, s, A, parent=None, parent_action=None, cost=0):
        '''
        s - the state defining the search tile
        A - list of actions
        parent - the parent search node
        parent_action - the action taken from parent to get to s
        '''
        self.parent = parent
        self.cost = cost
        self.parent_action = parent_action
        self.state = s[:]
        self.actions = A[:]

    def __str__(self):
        '''
        Return a human readable description of the node
        '''
        return str(self.state) + ' ' + str(self.actions)+' '+str(self.parent)+' '+str(self.parent_action)
    def __lt__(self, other):
        return self.cost < other.cost

class PriorityQ:
    '''
    Priority queue implementation with quick access for membership testing
    Setup currently to only with the SearchNode class
    '''
    def __init__(self):
        '''
        Initialize an empty priority queue
        '''
        self.l = [] # list storing the priority q
        self.s = set() # set for fast membership testing

    def __contains__(self, x):
        '''
        Test if x is in the queue
        '''
        return x in self.s

    def push(self, x, cost):
        '''
        Adds an element to the priority queue.
        If the state already exists, we update the cost
        '''
        if x.state in self.s:
            return self.replace(x, cost)
        heapq.heappush(self.l, (cost, x))
        self.s.add(x.state)

    def pop(self):
        '''
        Get the value and remove the lowest cost element from the queue
        '''
        x = heapq.heappop(self.l)
        self.s.remove(x[1].state)
        return x[1]

    def peak(self):
        '''
        Get the value of the lowest cost element in the priority queue
        '''
        x = self.l[0]
        return x[1]

    def __len__(self):
        '''
        Return the number of elements in the queue
        '''
        return len(self.l)

    def replace(self, x, new_cost):
        '''
        Removes element x from the q and replaces it with x with the new_cost
        '''
        for y in self.l:
            if x.state == y[1].state:
                self.l.remove(y)
                self.s.remove(y[1].state)
                break
        heapq.heapify(self.l)
        self.push(x, new_cost)

    def get_cost(self, x):
        '''
        Return the cost for the search node with state x.state
        '''
        for y in self.l:
            if x.state == y[1].state:
                return y[0]

    def __str__(self):
        '''
        Return a string of the contents of the list
        '''
        return str(self.l)

## determines what to do with the action
def tile_trans(s, a, player):
    '''
    Transition function for the current grid map.

    s - tuple describing the state as (row, col) position on the grid.
    a - the action to be performed from state s

    returns - s_prime, the state transitioned to by taking action a in state s.
    If the action is not valid (e.g. moves off the grid or into an obstacle)
    returns the current state.
    '''
    new_pos = list(s[:])                                                                            ## makes a copy of the state point and turns it into a list

    #print("a", a)                                                                                  ## used for debugging
    if a == 'x':                                                                                    ## if it goes into the X secret tunnel
        new_pos[_X] = int(player.Y_tile[_X])                                                        ## appear on the Y secret tunnel tile
        new_pos[_Y] = int(player.Y_tile[_Y])
    elif a == 'y':                                                                                  ## if it goes into the Y secret tunnel
        new_pos[_X] = int(player.X_tile[_X])                                                        ## appears on the X secret tunnel tile
        new_pos[_Y] = int(player.X_tile[_Y])
    elif a == 'u':                                                                                  ## if it goes up
        if s[_X] > 0:                                                                               ## make sure it doesn't go off the board
            if 'd' in tile_textures[player.map_data[new_pos[_X]-1][new_pos[_Y]]].quickinfo:         ## if the new tile has a down door to enter through
                new_pos[_X] -= 1                                                                    ## move up a tile
    elif a == 'd':                                                                                  ## if it goes down
        if s[_X] + 1 < len(player.map_data):                                                        ## make sure it doesn't go off the board
            if 'u' in tile_textures[player.map_data[new_pos[_X]+1][new_pos[_Y]]].quickinfo:         ## if the new tile has an up door to enter through    
                new_pos[_X] += 1                                                                    ## move down a tile
    elif a == 'l':
        if s[_Y] > 0:                                                                               ## make sure it doesn't go off the board
            if 'r' in tile_textures[player.map_data[new_pos[_X]][new_pos[_Y]-1]].quickinfo:         ## if the new tile has a right door to enter through     
                new_pos[_Y] -= 1                                                                    ## move right a tile
    elif a == 'r':
        if s[_Y] + 1 < len(player.map_data[0]):                                                     ## make sure it doesn't go off the board
            if 'l' in tile_textures[player.map_data[new_pos[_X]][new_pos[_Y]+1]].quickinfo:         ## if the new tile has a left door to enter through  
                new_pos[_Y] += 1                                                                    ## move left a tile
    else:                                                                                           ## if the action is not listed
        print('Unknown action:', str(a))                                                            ## let the user know what action it didn't understand
    
    s_prime = tuple(new_pos)                                                                        ## save the new position as a tuple
    return s_prime                                                                                  ## return the new position

def getting_path(tile):
    '''
    Function to determine the path that lead to the specified search node

    node - the SearchNode that is the end of the path

    returns - a tuple containing (path, action_path) which are lists respectively of the states
    visited from init to goal (inclusive) and the actions taken to make those transitions.
    '''
    path = []
    action_path = []
    
    while tile.parent:
        path.insert(0,tile.state)
        action_path.insert(0, tile.parent_action)
        tile = tile.parent
    path.insert(0, tile.state)
    print (action_path)
    print(path)
    return path

def astar(player, num_player = 1):
    #empty = []
    #n0 = tile_textures[player.map_data[player.row][player.column]]  
    n0 = SearchTile((player.row,player.column),tile_textures[player.map_data[player.row][player.column]].quickinfo)
    print("n0", n0)
    frontier = PriorityQ()
    visited = [] # visited nodes
    n0 = cost(n0) ### add cost to current node
    hcost = n0.cost + player.heuristic_map[n0.state[0]][n0.state[1]]
    frontier.push(n0, hcost)

    while len(frontier) > 0:
        #print("frontier", frontier)
        n_i = frontier.pop() 
        if(n_i.state not in visited):
            visited.append(n_i.state)
            Actions = tile_textures[player.map_data[n_i.state[_X]][n_i.state[_Y]]].quickinfo
            #empty.append(Actions)
            if is_goal(player.goal, n_i.state):
                #print("made it here")
                #print("quickinfo", empty)
                return getting_path(n_i), visited
            else:
                for a in Actions:
                    s_prime = tile_trans(n_i.state, a, player) ## transition funct
                    actions = tile_textures[player.map_data[s_prime[_X]][s_prime[_Y]]].quickinfo
                    n_prime = SearchTile(s_prime, actions, n_i, a) # Go to next column                    
                    n_prime = cost(n_prime)
                    hcost = n_prime.cost +  player.heuristic_map[n_prime.state[0]][n_prime.state[1]]
                    curcost = frontier.get_cost(n_prime)
                    if curcost == None or curcost > hcost:
                        frontier.push(n_prime,hcost)

    #print("no path found")
    #print("quickinfo", empty)
    return None, visited
