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
_X = 1
_Y = 0
_GOAL_COLOR = 0.75
_INIT_COLOR = 0.25
_PATH_COLOR_RANGE = _GOAL_COLOR-_INIT_COLOR
_VISITED_COLOR = 0.9

def cost(tile):
    if tile.parent is not None:
        if tile.quickinfo in _ACTIONS:
            tile.cost = 1+tile.parent.cost


    return tile

def heur(tile):
    
    yeppers = 2

    return tile + yeppers

def is_goal(player,goal):
    x=1


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

def tile_trans(self, s, a):
    '''
    Transition function for the current grid map.

    s - tuple describing the state as (row, col) position on the grid.
    a - the action to be performed from state s

    returns - s_prime, the state transitioned to by taking action a in state s.
    If the action is not valid (e.g. moves off the grid or into an obstacle)
    returns the current state.
    '''
    new_pos = list(s[:])
    # Ensure action stays on the board # Essentially a copy of Marks player move function

    if a == 'u':
        if s[_Y] > 0:
            new_pos[_Y] -= 1
    elif a == 'd':
        if s[_Y] < self.rows - 1:
            new_pos[_Y] += 1
    elif a == 'l':
        if s[_X] > 0:
            new_pos[_X] -= 1
    elif a == 'r':
        if s[_X] < self.cols - 1:
            new_pos[_X] += 1
    else:
        print('Unknown action:', str(a))

    # Test if new position is clear
    if self.occupancy_grid[new_pos[0], new_pos[1]]:
        s_prime = tuple(s)
    else:
        s_prime = tuple(new_pos)
    return s_prime

def astar(player, num_player = 1):
    empty = []
    n0 = tile_textures[player.map_data[player.row][player.column]] #tile at rowx coly SearchNode(init_state, _ACTIONS) ## the tile at the init_state location, 
    frontier = PriorityQ()
    visited = [] # visited nodes
    n0 = cost(n0) ### add cost to current node
    hcost = n0.cost + heur(n0) #### need to write heuristic function, use Mark's from player.py
    frontier.push(n0, hcost)

    while len(frontier) > 0:
        n_i = frontier.pop() 
        if(n_i.state not in visited):
            visited.append(n_i.state)

            if is_goal(n_i.state):
               return (backpath(n_i), visited)
            else:
                for a in _ACTIONS:
                    s_prime = tile_trans(n_i.state, a) ## transition funct
                    n_prime = SearchNode(s_prime,actions, n_i, a) # instead of creating a tile, just go to next tile
                    
                    n_prime = cost(n_prime)
                    hcost = n_prime.cost + heur(n_prime)
                    curcost = frontier.get_cost(n_prime)
                    if curcost == None or curcost > hcost:
                        frontier.push(n_prime,hcost)


    return ((empty, empty),visited)
