###### Graph Search ####### 

from asyncio.windows_events import NULL
import sys
import numpy as np
import heapq
import matplotlib.pyplot as plotter
from math import hypot, sqrt
from tilemap import *
# change to be in the form of new game
_ACTIONS = ['x', 'y', 'u','d','l','r', 'rt', 'bt', 'gt']

_X = 0                                                                          ## _X and 0 is row
_Y = 1                                                                          ## _Y and 1 is column


def cost(player, tile):
    if tile.parent is not None:
        if tile.parent in _ACTIONS:
            match tile.parent:                                                                                                                                  ## check the action item
                case "u":                                                                                                                                       ## if it was move up
                    tile.cost = 1+tile.parent.cost                                                                                                              ## add one to the cost
                case "d":                                                                                                                                       ## if it was move down
                    tile.cost = 1+tile.parent.cost                                                                                                              ## add one to the cost
                case "l":                                                                                                                                       ## if it was move left
                    tile.cost = 1+tile.parent.cost                                                                                                              ## add one to the cost
                case "r":                                                                                                                                       ## if it was move right
                    tile.cost = 1+tile.parent.cost                                                                                                              ## add one to the cost
                case "x":                                                                                                                                       ## if it was go through the x secret tunnel
                    tile.cost = 1+tile.parent.cost                                                                                                              ## add one to the cost
                case "y":                                                                                                                                       ## if it was go through the y secret tunnel
                    tile.cost = 1+tile.parent.cost                                                                                                              ## add one to the cost
                case "rt":                                                                                                                                      ## it was pick up a red token
                    tile.cost = 4 - player.Strength+tile.parent.cost                                                                                            ## adds cost (1 cost if Strength = 3, 2 cost is Strength = 2, 3 cost is Strength = 1)
                case "gt":                                                                                                                                      ## if it was pick up a red token
                    tile.cost = 4 - player.Agility+tile.parent.cost                                                                                             ## adds cost (1 cost if Agility = 3, 2 cost is Agility = 2, 3 cost is Agility = 1)
                case "bt":                                                                                                                                      ## if it was pick up blue token
                    tile.cost = 4 - player.Intelligence+tile.parent.cost                                                                                        ## adds cost (1 cost if Intelligence = 3, 2 cost is Intelligence = 2, 3 cost is Intelligence = 1)
                case "ret":                                                                                                                                     ## if it was break the red event token
                    tile.cost = 1+tile.parent.cost                                                                                                              ## add one to the cost
                case "get":                                                                                                                                     ## if it was break the green event token
                    tile.cost = 1+tile.parent.cost                                                                                                              ## add one to the cost
                case "bet":                                                                                                                                     ## if it was break the blue event token
                    tile.cost = 1+tile.parent.cost                                                                                                              ## add one to the cost
                case "foe":                                                                                                                                     ## if it was grab the fire of eidolon
                    tile.cost = 1+tile.parent.cost                                                                                                              ## add one to the cost

    return tile

## checks if the goal is the same as the state checking
def is_goal(goal,s):
    '''
    Test if a specifid state is the goal state

    s - tuple describing the state as (row, col) position on the grid.

    Returns - True if s is the goal. False otherwise.
    '''
    s = list(s)                                                                     ## turns this into a list so the two sides can compare

    return (s[_X] == goal[_X] and                                                   ## if the state's row and column equals the goal state and column return True, otherwise return False
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
def tile_trans(s, a, token, player):
    '''
    Transition function for the current grid map.

    s - tuple describing the state as (row, col) position on the grid.
    a - the action to be performed from state s

    returns - s_prime, the state transitioned to by taking action a in state s.
    If the action is not valid (e.g. moves off the grid or into an obstacle)
    returns the current state.
    '''
    new_pos = list(s[:])                                                                                                ## makes a copy of the state point and turns it into a list

    #print("a", a)                                                                                                      ## used for debugging
    match a:
        case 'x':                                                                                                       ## if it goes into the X secret tunnel
            new_pos[_X] = int(player.Y_tile[_X])                                                                        ## appear on the Y secret tunnel tile
            new_pos[_Y] = int(player.Y_tile[_Y])
        case 'y':                                                                                                       ## if it goes into the Y secret tunnel
            new_pos[_X] = int(player.X_tile[_X])                                                                        ## appears on the X secret tunnel tile
            new_pos[_Y] = int(player.X_tile[_Y])
        case 'u':                                                                                                       ## if it goes up
            if s[_X] > 0:                                                                                               ## make sure it doesn't go off the board
                if 'd' in tile_textures[player.map_data[new_pos[_X]-1][new_pos[_Y]]].quickinfo:                         ## if the new tile has a down door to enter through
                    new_pos[_X] -= 1                                                                                    ## move up a tile
        case 'd':                                                                                                       ## if it goes down
            if s[_X] + 1 < len(player.map_data):                                                                        ## make sure it doesn't go off the board
                if 'u' in tile_textures[player.map_data[new_pos[_X]+1][new_pos[_Y]]].quickinfo:                         ## if the new tile has an up door to enter through    
                    new_pos[_X] += 1                                                                                    ## move down a tile
        case 'l':
            if s[_Y] > 0:                                                                                               ## make sure it doesn't go off the board
                if 'r' in tile_textures[player.map_data[new_pos[_X]][new_pos[_Y]-1]].quickinfo:                         ## if the new tile has a right door to enter through     
                    new_pos[_Y] -= 1                                                                                    ## move right a tile
        case 'r':
            if s[_Y] + 1 < len(player.map_data[0]):                                                                     ## make sure it doesn't go off the board
                if 'l' in tile_textures[player.map_data[new_pos[_X]][new_pos[_Y]+1]].quickinfo:                         ## if the new tile has a left door to enter through  
                    new_pos[_Y] += 1                                                                                    ## move left a tile
        case 'rt':                                                                                                      ## if pick up red token
            token[0] += 1                                                                                               ## increase the collected red tokens by 1
        case 'gt':                                                                                                      ## if pick up green token
            token[1] += 1                                                                                               ## increase the collected green tokens by 1
        case 'bt':                                                                                                      ## if pick up blue token
            token[2] += 1                                                                                               ## increase the collected blue tokens by 1
        case _:                                                                                                         ## if the action is not listed
            print('Unknown action:', str(a))                                                                            ## let the user know what action it didn't understand
    
    s_prime = tuple(new_pos)                                                                                            ## save the new position as a tuple
    return s_prime, token                                                                                               ## return the new position


## determines the path to the goal and the actions taken to get there
def getting_path(tile):
    '''
    Function to determine the path that lead to the specified search node

    node - the SearchNode that is the end of the path

    returns - a tuple containing (path, action_path) which are lists respectively of the states
    visited from init to goal (inclusive) and the actions taken to make those transitions.
    '''
    path = []                                                                                                           ## initalizes the path
    action_path = []                                                                                                    ## inializes the order of actiosn
    
    while tile.parent:                                                                                                  ## if the tile has a parent
        path.insert(0,tile.state)                                                                                       ## adds the tile.state to the path
        action_path.insert(0, tile.parent_action)                                                                       ## adds the action take to get to tile state
        tile = tile.parent                                                                                              ## sets the next tile to be the tile's parent
    path.insert(0, tile.state)                                                                                          ## adds the tile wihtout a parent to the path
    print ("action_path", action_path)                                                                                  ## prints out the action's taken (used fod debugging)
    print("path", path)                                                                                                 ## prints out the planned path (used fod debugging)
    return path, action_path                                                                                            ## returns the planned path and the actions taken


## uses A* planning in order to determine the shortest path to a goal
def astar(player, goal, num_player = 1):
    token = [player.Red_Token, player.Green_Token, player.Blue_Token]
    n0 = SearchTile((player.row,player.column),tile_textures[player.map_data[player.row][player.column]].quickinfo)     ## sets the SearchTile as the quickinfo from the tile in question
    print("n0", n0)                                                                                                     ## used for debugggin
    frontier = PriorityQ()                                                                                              ## 
    visited = []                                                                                                        ## initalizes visited nodes    
    n0 = cost(player, n0)                                                                                               ## add cost to current node
    hcost = n0.cost + player.heuristic_map[n0.state[0]][n0.state[1]]                                                    ## combines the heuristic value and the cost
    frontier.push(n0, hcost)                                                                                            ## 

    while len(frontier) > 0:                                                                                            ##
        #print("frontier", frontier)                                                                                     ## used for debugging
        n_i = frontier.pop()                                                                                            ## 
        if(n_i.state not in visited):                                                                                   ## if the state hasen't been visited before
            visited.append(n_i.state)                                                                                   ## adds the state to the visited states
            Actions = tile_textures[player.map_data[n_i.state[_X]][n_i.state[_Y]]].quickinfo                            ## grabs the possible actions
            if is_goal(goal, n_i.state):                                                                                ## if we are at the goal
                path, action_path = getting_path(n_i)                                                                   ## gets the planned path and the actions to take to that path
                return path, action_path, visited                                                                       ## returns the planned path, the actions to take, and the visited lists
            else:                                                                                                       ## otherwise
                for a in Actions:                                                                                       ## for each actions 
                    s_prime, temp_token = tile_trans(n_i.state, a, token, player)                                       ## transition funct
                    actions = tile_textures[player.map_data[s_prime[_X]][s_prime[_Y]]].quickinfo                        ## 
                    n_prime = SearchTile(s_prime, actions, n_i, a)                                                      ## determines the cost it would be to get to this tile                    
                    n_prime = cost(player, n_prime)                                                                     ## gets the cost of the action
                    hcost = n_prime.cost +  player.heuristic_map[n_prime.state[0]][n_prime.state[1]]                    ## combines the heuristic value and the cost
                    curcost = frontier.get_cost(n_prime)                                                                ## get the current cost of the action
                    if curcost == None or curcost > hcost:                                                              ## if there isn't a current cost or if the new cost is less than the current cost
                        frontier.push(n_prime,hcost)                                                                    ## make the cost of the action the new cost
                        token = temp_token

    #print("no path found")                                                                                              ## used for debugging
    #print("quickinfo", empty)                                                                                           ## used for debugging
    return None, None, visited                                                                                          ## return only the visted points
