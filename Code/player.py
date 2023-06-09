# Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/player.py
import pygame
import time
import settings
import automove
import numpy as np
from tilemap import *
import matplotlib.pyplot as plotter
from math import hypot, sqrt
from graph_search import astar
from pynput.keyboard import Key, Controller

controller = Controller()
TILE_SIZE = settings.TILE_SIZE  ## Gets the size of the tile from the settings file and sets it as a global variable

##############################################################################################################################################################################################################################
#### Things to add to player
####    - Have the player build the map as they go
####    - Have A* work with tokens
##############################################################################################################################################################################################################################

def create_player_texture(name):
    image = pygame.transform.scale(name,(TILE_SIZE/2,TILE_SIZE/2))                                                                                              ## scales the image to 1/4 of a tile size
    return image                                                                                                                                                ## return the token image


## Creates a player
class Player(pygame.sprite.Sprite):                                                
    def __init__(self, sprites_group, map_data, STR, INT, DEX, living = False):
        self.groups = sprites_group                                                                                                                             ##
        pygame.sprite.Sprite.__init__(self, self.groups)                                                                                                        ##
        self.map_data = map_data                                                                                                                                ## stores the map for the player
        self.image = pygame.image.load("Images/Other/magic_meeple_games_makshift_token.png")                                                                    ## sets the players image and loads the file
        self.image = create_player_texture(self.image)                                                                                                          ## scales the image for use
        self.rect = self.image.get_rect()                                                                                                                       ## get the rectangle angle fo the surface
        self.Strength = STR                                                                                                                                       ## determines the players strength 
        self.Intelligence = INT                                                                                                                                   ## determines the players intelligence
        self.Agility = DEX                                                                                                                                        ## determines the players Agility
        self.start_point = np.where(map_data == 1)                                                                                                              ## determines where the starting point is on the map
        self.end = np.where(map_data == 6)                                                                                                                      ## determines where the end tile is
        self.goal = [int(self.end[0]),int(self.end[1])]                                                                                                         ## determien a goal tile
        self.X_tile = np.where(map_data == 7)                                                                                                                   ## determines where the secret X tile is on the map
        self.Y_tile = np.where(map_data == 8)                                                                                                                   ## determines where the secret Y tile is on the map
        self.row = int(self.start_point[0])                                                                                                                     ## This is the row the player is at
        self.column = int(self.start_point[1])                                                                                                                  ## This is the column the player is at
        self.adjust = len(settings.Players)*10
        self.rect.centerx = self.adjust+self.column*TILE_SIZE + TILE_SIZE/3                                                                                     ## places the player at the starting point's x position
        self.rect.centery = self.row*TILE_SIZE + TILE_SIZE/2                                                                                                    ## places the player at the starting point's y position
        self.Green_Token = 0                                                                                                                                    ## initalizes the green token count
        self.Red_Token = 0                                                                                                                                      ## initalizes the red token count
        self.Blue_Token = 0                                                                                                                                     ## initalizes the blue token count
        self.FireofEidolon = 0                                                                                                                                  ## initalizes the grabbing of the Fire of Eidolon
        self.visited = [[self.row, self.column]]                                                                                                                ## keeps track of the locations visited (starting with the starting points)
        self.actions = ["S"]                                                                                                                                    ## keeps track of actions taken (starting with S for Start)
        self.totalcost = 0                                                                                                                                      ## keeps track of the total cost
        self.heuristic_map_maker(self.goal)                                                                                                                     ## sets up the heruistic map
        self.active = True
        self.otherplayer = None
        self.keycount = 3
        self.plans = []
        self.todo = []
        self.explored = []
        self.moving = False
        settings.Players.append(self)
        self.goalUpdate()

    def update(self):                                                                                                                                           ## update things if a key is presed
        self.get_event()                                                                                                                                        ## checks if a key was presed


    def get_event(self):
        keys = pygame.key.get_pressed() 
        if self.active == True:
            if self.moving == True:
                controller.press('7')
                if self.keycount < 3:
                    self.auto()
                else:
                    self.moving = False
                time.sleep(0.25)                                                                                                                                     ## gives the computer a time before reading the next keystroke   
                controller.release('7')
            else:
                if self.keycount == 3:
                    controller.press('7')
                    self.active = False
                    if self.moving == True:
                        print('AUTOMOVE DONE!')  
                        self.moving = False
                    self.keycount = 0
                    pygame.event.clear()
                    if self.otherplayer != None:
                        self.otherplayer.active = True
                        self.otherplayer.goalUpdate()
                        if self.otherplayer.plans != None:                                                                                                                              ## if a path to the goal is found
                            settings.planning = True                                                                                                                        ## let the global know that a planning path was found
                        settings.Active_Player = self.otherplayer                                                                                                                            ## sets player 1 as itself
                        settings.seen = True                                                                                                                                ## lets the global know that it has a set of explored (visited) points
                    time.sleep(0.25)                                                                                                                                     ## gives the computer a time before reading the next keystroke   

                    controller.release('7') 
                elif settings.selfplay == True:
                    controller.press('7')
                    if self.keycount < 3:
                        self.auto()
                    time.sleep(0.25)                                                                                                                                     ## gives the computer a time before reading the next keystroke   
                    controller.release('7') 

            #keys = pygame.key.get_pressed()                                                                                                                         ## check what key got pressed
            #if (keys[pygame.K_s] or keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_d]
            #    or keys[pygame.K_q]):
            #    self.keycount += 1
            if keys[pygame.K_u]:
                settings.selfplay = True

            if keys[pygame.K_l]:                                                                                                                                    ## allows the player to skip an action without moving
                self.keycount += 1                                                                                                                                  ## passes there action
                time.sleep(0.5)                                                                                                                                     ## gives the computer a time before reading the next keystroke   
                
            ## Moving Up
            if keys[pygame.K_w]:                                                                                                                                    ## when the "W" button is pressed
                if 'u' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                    if self.row-1 >= 0:                                                                                                                             ## makes sure player doesn't walk off edge
                        if 'd' in tile_textures[self.map_data[self.row-1][self.column]].quickinfo:
                            self.actions.append("U")                                                                                                                ## remembers it moved up
                            self.move(0, -TILE_SIZE)
                            self.keycount += 1

            ## Moving Down
            if keys[pygame.K_s]:
                if 'd' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                    if self.row+1 < len(self.map_data):                                                                                                             ## makes sure player doesn't walk off edge
                        if 'u' in tile_textures[self.map_data[self.row+1][self.column]].quickinfo:
                            self.actions.append("D")                                                                                                                ## remembers it moved down
                            self.move(0, +TILE_SIZE)
                            self.keycount += 1
            ## Moving Left
            if keys[pygame.K_a]:
                if 'l' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                    if self.column-1 >= 0:                                                                                                                          ## makes sure player doesn't walk off edge
                        if 'r' in tile_textures[self.map_data[self.row][self.column-1]].quickinfo:
                            self.actions.append("L")                                                                                                                ## remembers it moved left
                            self.move(-TILE_SIZE, 0)
                            self.keycount += 1
            ## Moving Right
            if keys[pygame.K_d]:
                if 'r' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                    if self.column+1 < len(self.map_data[0]):                                                                                                       ## makes sure player doesn't walk off edge
                        if 'l' in tile_textures[self.map_data[self.row][self.column+1]].quickinfo:
                            self.actions.append("R")                                                                                                                ## remembers it moved right
                            self.move(+TILE_SIZE, 0)
                            self.keycount += 1

            ## set goal
            if keys[pygame.K_g]:
                #self.goal = [self.row,self.column]                                                                                                                 ## sets the tile the player is currently at as the goal (used for debugging)
                self.goalUpdate()                                                                                                                                   ## updates on what your next goal should be

            ## ressts everything
            if keys[pygame.K_r]:
                settings.planning = False                                                                                                                           ## resets the global planning
                settings.seen = False                                                                                                                               ## resets teh global seen

            ## A-Star to somewhere
            if keys[pygame.K_p]:
                settings.planning = False                                                                                                                           ## resets the global planning
                settings.seen = False                                                                                                                               ## resets teh global seen
                self.goalUpdate()                                                                                                                                   ## updates on what your next goal should be along with the A* planning to get to said goal
                self.heuristic_map_maker(self.goal)                                                                                                                 ## updates the heruistic map

                ## performs the astar formula
                #print("plans", self.plans)                                                                                                                          ## prints the planned states of path to the goal
                #print("explored", self.explored)                                                                                                                    ## prints the explored (visited) states to find path
                if self.plans != None:                                                                                                                              ## if a path to the goal is found
                    settings.planning = True                                                                                                                        ## let the global know that a planning path was found
                settings.Active_Player = self                                                                                                                            ## sets player 1 as itself
                settings.seen = True                                                                                                                                ## lets the global know that it has a set of explored (visited) points
                time.sleep(0.5)                                                                                                                                     ## gives the computer a time before reading the next keystroke   

            ## Grabs tokens
            if keys[pygame.K_e]:                                                                                                                                    ## when the "E" button is pressed
                if tile_textures[self.map_data[self.row][self.column]].token != None:                                                                               ## If there is a tile there
                    match tile_textures[self.map_data[self.row][self.column]].type:                                                                                 ## determine what the tile type is
                        case "Red":                                                                                                                                 ## if it's listed as red
                            if (4 - self.Strength + self.keycount) <= 3:
                                self.keycount = 4 - self.Strength + self.keycount
                                self.totalcost = 4 - self.Strength + self.totalcost                                                                                     ## adds cost (1 cost if Strength = 3, 2 cost is Strength = 2, 3 cost is Strength = 1)
                                settings.total_actions_value = 4 - self.Strength + settings.total_actions_value
                                self.Red_Token = self.Red_Token + 1                                                                                                     ## increase the Red_Token by 1
                                settings.total_Red_Tokens += 1
                                tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                                tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("rt")                                                              ## Removes the token from quick info
                        case "Green":                                                                                                                               ## if it's listed as green
                            if (4 - self.Agility + self.keycount) <= 3:
                                self.keycount = 4 - self.Agility + self.keycount
                                self.totalcost = 4 - self.Agility + self.totalcost                                                                                      ## adds cost (1 cost if Agility = 3, 2 cost is Agility = 2, 3 cost is Agility = 1)
                                settings.total_actions_value = 4 - self.Agility + settings.total_actions_value
                                self.Green_Token = self.Green_Token + 1                                                                                                 ## increase the Green_Token by 1
                                settings.total_Green_Tokens += 1
                                tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                                tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("gt")                                                              ## Removes the token from quick info  
                        case "Blue":                                                                                                                                ## if it's listed as blue
                            if (4 - self.Intelligence + self.keycount) <= 3:
                                self.keycount = 4 - self.Intelligence + self.keycount
                                self.totalcost = 4 - self.Intelligence + self.totalcost                                                                                 ## adds cost (1 cost if Intelligence = 3, 2 cost is Intelligence = 2, 3 cost is Intelligence = 1)
                                settings.total_actions_value = 4 - self.Intelligence + settings.total_actions_value
                                self.Blue_Token = self.Blue_Token + 1                                                                                                   ## increase the Blue_Token by 1
                                settings.total_Blue_Tokens += 1
                                tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                                tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("bt")                                                              ## Removes the token from quick info
                        case "RedEvent":                                                                                                                            ## if it's listed as red event
                            if self.Red_Token >= 6 or settings.total_Red_Tokens >= 6:                                                                                                                 ## do you have enough tokens to break the red event
                                self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to break event
                                self.keycount += 1
                                settings.total_actions_value += 1
                                settings.Red_Event_Broken = True                                                                                                    ## breaks the red event
                                tile_textures[self.map_data[self.row][self.column]].type = "Broken_RedEvent"                                                        ## displays the broken red event token
                                tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                                tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("ret")                                                         ## Removes the token from quick info
                                self.Red_Token = 0
                        case "GreenEvent":                                                                                                                          ## if it's listed as green event 
                            if self.Green_Token >= 6 or settings.total_Green_Tokens >= 6:                                                                                                               ## do you have enough tokens to break the green event
                                self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to break event
                                self.keycount += 1
                                settings.total_actions_value += 1
                                settings.Green_Event_Broken = True                                                                                                  ## breaks the green event
                                tile_textures[self.map_data[self.row][self.column]].type = "Broken_GreenEvent"                                                      ## displays the broken green event token
                                tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                                tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("get")                                                         ## Removes the token from quick info
                                self.Green_Token = 0
                        case "BlueEvent":                                                                                                                           ## if it's listed as blue event
                            if self.Blue_Token >= 6 or settings.total_Blue_Tokens >= 6:                                                                                                                ## do you have enough tokens to break the blue event
                                self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to break event
                                settings.total_actions_value += 1
                                settings.Blue_Event_Broken = True                                                                                                   ## breaks the blue event
                                tile_textures[self.map_data[self.row][self.column]].type = "Broken_BlueEvent"                                                       ## displays the broken blue event token
                                tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                                tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("bet")                                                         ## Removes the token from quick info
                                self.Blue_Token = 0
                                self.keycount += 1
                        case "FireofEidolon":                                                                                                                       ## if it's listed as Fire of Eidolon
                            if settings.Red_Event_Broken == True and settings.Green_Event_Broken == True and settings.Blue_Event_Broken == True:                    ## all other events broken?
                                self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to grab Fire of Eidolon
                                self.keycount += 1
                                settings.total_actions_value += 1
                                settings.FireofEidolon_Grabbed = True                                                                                               ## marks that the Fire of Eidolon has been grabbed
                                self.FireofEidolon = 1                                                                                                              ## indicates that the player has the Fire of Eidolon
                                tile_textures[self.map_data[self.row][self.column]].token = None                                                                    ## Removes the token
                                tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("foe")                                                         ## Removes the token from quick info
                    self.goalUpdate()                                                                                                                              ## updates on what your next goal should be
                    #print(self.totalcost)                                                                                                                           ## used for debugging 
                    self.actions.append("T")                                                                                                                        ## remembers it grabbed a token (or at least tired)
                time.sleep(0.5)                                                                                                                                     ## gives the computer a time before reading the next keystroke   

            ## Use Tunnel
            if keys[pygame.K_q]:                                                                                                                                    ## when the "Q" button is pressed
                if tile_textures[self.map_data[self.row][self.column]].name == "SecretX":                                                                           ## if on secret X tile              
                    self.row = int(self.Y_tile[0])                                                                                                                  ## This is the row the player is at
                    self.column = int(self.Y_tile[1])                                                                                                               ## This is the column the player is at
                    self.rect.centerx = self.adjust + self.column*TILE_SIZE + TILE_SIZE/3                                                                           ## places the player at the Secret Y's x position
                    self.rect.centery = self.row*TILE_SIZE + TILE_SIZE/2                                                                                            ## places the player at the Secret Y's y position
                    self.actions.append("X")                                                                                                                        ## Used the secret X tunnel
                    self.move(0, 0)                                                                                                                                 ## records where the player went
                    self.keycount += 1
                elif tile_textures[self.map_data[self.row][self.column]].name == "SecretY":                                                                         ## if on a secret Y tile                  
                    self.row = int(self.X_tile[0])                                                                                                                  ## This is the row the player is at
                    self.column = int(self.X_tile[1])                                                                                                               ## This is the column the player is at
                    self.rect.centerx = self.adjust + self.column*TILE_SIZE + TILE_SIZE/3                                                                           ## places the player at the Secret Y's x position
                    self.rect.centery = self.row*TILE_SIZE + TILE_SIZE/2                                                                                            ## places the player at the Secret Y's y position
                    self.actions.append("Y")                                                                                                                        ## Used the secret Y tunnel
                    self.move(0, 0)                                                                                                                                 ## records where the player went
                    self.keycount += 1
                #print(self.totalcost)                                                                                                                               ## used for debugging fro
                time.sleep(0.5)                                                                                                                                     ## gives the computer a time before reading the next keystroke
    
            if keys[pygame.K_b]:
                print('Automoving...')
                self.moving = True
                time.sleep(0.5)

    def goalUpdate(self):
        goal = [0,0]                                                                                                                                            ## initalizes the goal

        if settings.Red_Event_Broken == True and settings.Green_Event_Broken == True and settings.Blue_Event_Broken == True:                                    ## if all the event tokens were grabbed
            tile = np.where(self.map_data == 2)                                                                                                                 ## to search by tile type
            goal[0] = int(tile[0][-1])                                                                                                                          ## sets the row of the point
            goal[1] = int(tile[1][-1])
            self.heuristic_map_maker(goal)                                                                                                                      ## makes a heuristic map for the Fire of Eidolon tile
            self.plans, self.todo, self.explored = astar(self, goal)                                                                                            ## compute the A* algorithm to find the shortest path to the goal
        else:
            self.make_token_map()                                                                                                                                   ## makes a map of the remaining tokens
            #print("token map", settings.token_map)                                                                                                                 ## used for debugging
            #print("red token locations", settings.red_token_locations)
            #print("green token locations", settings.green_token_locations)
            #print("blue token locations", settings.blue_token_locations)

            red = np.where(self.map_data == 3)                                                                                                                      ## gets the red event tile 
            green = np.where(self.map_data == 4)                                                                                                                    ## gets the green event tile 
            blue = np.where(self.map_data == 5)                                                                                                                     ## gets the blue event tile 
            red_cal_cost = 1000000                                                                                                                                  ## initalizes the red calculated costs
            green_cal_cost = 1000000                                                                                                                                ## initalizes the green calculated costs
            blue_cal_cost = 1000000                                                                                                                                 ## initalizes the blue calculated costs
            attributes = [self.Strength, self.Intelligence, self.Agility]                                                                                           ## puts all the ability scores in an index
            if self.Red_Token > 5 or settings.total_Red_Tokens > 5:                                                                                                 ## if enough red tokens have been grabbed
                attributes[0] = -1                                                                                                                                  ## don't try to go for that color
            if self.Blue_Token > 5 or settings.total_Blue_Tokens > 5:                                                                                               ## if enough green tokens have been grabbed
                attributes[1] = -1                                                                                                                                  ## don't try to go for that color
            if self.Green_Token > 5 or settings.total_Green_Tokens > 5:                                                                                             ## if enough blue tokens have been grabbed
                attributes[2] = -1                                                                                                                                  ## don't try to go for that color

            ind_num = attributes.index(max(attributes))
            match ind_num:
                case 0:
                    closest_token = [0, 0]
                    lowest_token_cost = 100000
                    for i in range(len(settings.red_token_locations)):
                        self.heuristic_map_maker(settings.red_token_locations[i])
                        token_states, token_actionpath, token_explored = astar(self, settings.red_token_locations[i])
                        token_cal_cost, token_planned_r, token_planned_g, token_planned_b = self.cost_calulator(token_actionpath)
                        if lowest_token_cost == 100000 or token_cal_cost < lowest_token_cost:
                            closest_token = settings.red_token_locations[i]
                            lowest_token_cost = token_cal_cost
                            least_states = token_states
                            lest_action = token_actionpath
                            least_explored = token_explored  
                            print("red closest_token", closest_token)
                case 1:
                    closest_token = [0, 0]
                    lowest_token_cost = 100000
                    for i in range(len(settings.blue_token_locations)):
                        self.heuristic_map_maker(settings.blue_token_locations[i])
                        token_states, token_actionpath, token_explored = astar(self, settings.blue_token_locations[i])
                        token_cal_cost, token_planned_r, token_planned_g, token_planned_b = self.cost_calulator(token_actionpath)
                        if lowest_token_cost == 100000 or token_cal_cost < lowest_token_cost:
                            closest_token = settings.blue_token_locations[i]
                            lowest_token_cost = token_cal_cost
                            least_states = token_states
                            lest_action = token_actionpath
                            least_explored = token_explored  
                            print("blue closest_token", closest_token)
                case 2:
                    closest_token = [0, 0]
                    lowest_token_cost = 100000
                    for i in range(len(settings.green_token_locations)):
                        self.heuristic_map_maker(settings.green_token_locations[i])
                        token_states, token_actionpath, token_explored = astar(self, settings.green_token_locations[i])
                        token_cal_cost, token_planned_r, token_planned_g, token_planned_b = self.cost_calulator(token_actionpath)
                        if lowest_token_cost == 100000 or token_cal_cost < lowest_token_cost:
                            closest_token = settings.green_token_locations[i]
                            lowest_token_cost = token_cal_cost
                            least_states = token_states
                            lest_action = token_actionpath
                            least_explored = token_explored  
                            print("green closest_token", closest_token)

            if settings.Red_Event_Broken == False and (self.Red_Token > 5 or settings.total_Red_Tokens > 5):                                                                                                              ## red event broken false
                goal[0] = int(red[0][-1])                                                                                                                       ## sets the row of the potential goal point
                goal[1] = int(red[1][-1])
                self.heuristic_map_maker(goal)                                                                                                                  ## makes a heuristic map for the red event tile
                red_states, red_actionpath, red_explored = astar(self, goal)                                                                                    ## compute the A* algorithm for red_event tile
                red_cal_cost, red_planned_r, red_planned_g, red_planned_b = self.cost_calulator(red_actionpath)                                                 ## calculates the cost of the shortest path
            else:
                red_cal_cost = 100000

            if settings.Green_Event_Broken == False and (self.Green_Token > 5 or settings.total_Green_Tokens > 5):                                                                                                            ## green event broken false
                goal[0] = int(green[0][-1])                                                                                                                     ## sets the row of the potential goal point
                goal[1] = int(green[1][-1])
                self.heuristic_map_maker(goal)                                                                                                                  ## makes a heuristic map for the green event tile
                green_states, green_actionpath, green_explored = astar(self, goal)                                                                              ## compute the A* algorithm for green_event tile
                green_cal_cost, green_planned_r, green_planned_g, green_planned_b = self.cost_calulator(green_actionpath)                                       ## calculates the cost of the shortest path
            else:
                green_cal_cost = 100000

            if settings.Blue_Event_Broken == False and (self.Blue_Token > 5 or settings.total_Blue_Tokens > 5):                                                                                                             ## blue event broken false
                goal[0] = int(blue[0][-1])                                                                                                                      ## sets the row of the potential goal point
                goal[1] = int(blue[1][-1])
                self.heuristic_map_maker(goal)                                                                                                                  ## makes a heuristic map for the blue event tile
                blue_states, blue_actionpath, blue_explored = astar(self, goal)                                                                                 ## compute the A* algorithm for green_event tile
                blue_cal_cost, blue_planned_r, blue_planned_g, blue_planned_b = self.cost_calulator(blue_actionpath)                                            ## calculates the cost of the shortest path
            else:
                blue_cal_cost = 100000

            #print("red_cal_cost, green_cal_cost, blue_cal_cost", red_cal_cost, green_cal_cost, blue_cal_cost)
            comparer = (red_cal_cost, green_cal_cost, blue_cal_cost, lowest_token_cost)                                                                         ## preps to compare the three calculated costs
            small_index = comparer.index(min(comparer))                                                                                                         ## what is the index number of the smallest  calculated costs
            if red_cal_cost == comparer[small_index] and red_cal_cost != 100000:                                                                                                           ## if the value of the red_cal_cost is equal to the smallest recorded
                goal[0] = int(red[0][-1])                                                                                                                   ## sets the row of the point
                goal[1] = int(red[1][-1])
                self.plans = red_states                                                                                                                     ## sets the plans to be the list of red states
                self.todo = red_actionpath                                                                                                                  ## sets the todo list to be the planned red actionpath
                self.explored = red_explored                                                                                                                ## sets the list of explored to the list of red explored
            elif green_cal_cost == comparer[small_index] and green_cal_cost != 100000:                                                                                                       ## else if the value of the green_heuristic is equal to the smallest recorded
                goal[0] = int(green[0][-1])                                                                                                                 ## sets the row of the point
                goal[1] = int(green[1][-1])
                self.plans = green_states                                                                                                                   ## sets the plans to be the list of green states
                self.todo = green_actionpath                                                                                                                ## sets the todo list to be the planned green actionpath
                self.explored = green_explored                                                                                                              ## sets the list of explored to the list of green explored
            elif blue_cal_cost == comparer[small_index] and blue_cal_cost != 100000:                                                                                                        ## else if the value of the blue_cal_cost is equal to the smallest recorded
                goal[0] = int(blue[0][-1])                                                                                                                  ## sets the row of the point
                goal[1] = int(blue[1][-1])
                self.plans = blue_states                                                                                                                    ## sets the plans to be the list of blue states
                self.todo = blue_actionpath                                                                                                                 ## sets the todo list to be the planned blue actionpath
                self.explored = blue_explored                                                                                                               ## sets the list of explored to the list of blue explored
            elif lowest_token_cost == comparer[small_index] and lowest_token_cost != 100000:
                print("closest token", closest_token)
                goal = closest_token
                self.plans = least_states
                self.todo = lest_action
                self.explored = least_explored
                print("goal", goal)
        self.todo.append('t')
        if settings.FireofEidolon_Grabbed:                                                                                                                      ## If the Fire of Eidolon was Grabbed
            goal = [int(self.end[0]),int(self.end[1])]                                                                                                          ## set the goal to be the end tile
            self.heuristic_map_maker(goal)                                                                                                                      ## makes a heuristic map for the End tile
            self.plans, self.todo, self.explored = astar(self, goal)                                                                                            ## compute the A* algorithm to find the shortest path to the goal  
        print("goal", goal)
        self.goal = goal                                                                                                                                        ## sets the players goal to the new goal
        print("self.goal", self.goal)
        self.heuristic_map_maker(goal)                                                                                                                          ## reset the heuristic map
        if self.plans != None:                                                                                                                              ## if a path to the goal is found
            settings.planning = True                                                                                                                        ## let the global know that a planning path was found
        settings.Active_Player = self                                                                                                                            ## sets player 1 as itself
        settings.seen = True                                                                                                                                ## lets the global know that it has a set of explored (visited) points
  

    ## moves the player on the screen and where the player is on the map
    def move(self, dx, dy):
        self.totalcost = self.totalcost + 1                                                                                                                     ## adds 1 to the total cost
        settings.total_actions_value += 1                                                                                                                       ## updates the total actions value of all players
        #print(self.totalcost)                                                                                                                                   ## used for debugging
        self.rect.x += dx                                                                                                                                       ## lets the compter know where to move the player in the x direction
        self.rect.y += dy                                                                                                                                       ## lets the compter know where to move the player in the y direction
        self.row = self.row + dy//TILE_SIZE                                                                                                                     ## sets the new row
        self.column = self.column + dx//TILE_SIZE                                                                                                               ## sets the new column
        self.visited.append([self.row, self.column])                                                                                                            ## saves the tile visited
        if tile_textures[self.map_data[self.row][self.column]].name == "EndTile" and self.FireofEidolon == 1:                                                   ## if the player is on the End Tile and has the Fire of Eidolon
            settings.planning = False                                                                                                                           ## turns off planning path so it doesn't overlap with final backpath
            settings.seen = False                                                                                                                               ## turns off visted so it doesn't overlap with final backpath
            settings.Win = True
            print("You Win!")                                                                                                                                   ## let the player know they won
            print("Vistied Sets of this Player", self.visited)                                                                                                  ## displays the visited tiles in order of vist
            print("Actions Player_1", self.actions)                                                                                                             ## displays the actions in order of taken
            print("Total Cost", settings.total_actions_value)                                                                                                   ## displays the total costs to win
        time.sleep(0.5)                                                                                                                                         ## gives the computer a time before reading the next keystroke

    ## Calculating the euclidean heuristic value between two points
    def euclidean_heuristic(self, row, column,  tile_num, D = 1):
        if tile_num != 0:                                                                                                                                       ## skip if the goal is 0
            point = [0,0]                                                                                                                                       ## initalizes the point
            tile = np.where(self.map_data == tile_num)                                                                                                          ## to search by tile type
            point[0] = int(tile[0][-1])                                                                                                                         ## sets the row of the point
            point[1] = int(tile[1][-1])                                                                                                                         ## sets the column of the point
            dis = D*(sqrt((row-point[0])**2 + (column-point[1])**2))                                                                                            ## cacluate the euclidean huristic between the player point and the tile number goal
        else:                                                                                                                                                   ## if tile looking for is 0
            dis = 10000000                                                                                                                                      ## just set the distance to 10000000 (impossible)
        return dis                                                                                                                                              ## return the distance calculated

    ## Calculating the manhattan heuristic value between two points
    def manhattan_heuristic(self, row, column,  tile_num, D = 1):
        if tile_num != 0:                                                                                                                                       ## skip if the goal is 0
            point = [0,0]                                                                                                                                       ## initalizes the point
            tile = np.where(self.map_data == tile_num)                                                                                                          ## to search by tile type
            point[0] = int(tile[0][-1])                                                                                                                         ## sets the row of the point
            point[1] = int(tile[1][-1])                                                                                                                         ## sets the column of the point
            dis = D*(abs(row-point[0]) + abs(column-point[1]))                                                                                                  ## cacluate the manhattan huristic between the player point and the tile number goal
        else:                                                                                                                                                   ## if tile looking for is 0
            dis = 10000000                                                                                                                                      ## just set the distance to 10000000 (impossible)
        return dis                                                                                                                                              ## return the distance calculated

    def heuristic_map_maker(self, goal):
        secret_heuristic = []                                                                                                                                   ## initalizes the hurisitc_map from the farther secret tile
        self.heuristic_map = []                                                                                                                                 ## initalizes the huristic_map
        secret_goal_heuristic = []
        goal_heuristic_map = []

        ## creates the initial heuritic map in reference to the player location
        for i in range(len(self.map_data)):                                                                                                                     ## for each of the rows                                                                 
            self.heuristic_map.append([])                                                                                                                       ## initalize space for columns
            for j in range(len(self.map_data[0])):                                                                                                              ## for each column
                self.heuristic_map[i].append(self.manhattan_heuristic(self.row, self.column, self.map_data[i][j]))                                              ## determine the euclidean heuristic in reference to the location of the player (use another heurtistic?)

        #print("heuristic_map ", self.heuristic_map)                                                                                                             ## used for debugging

        X_heuristic = self.heuristic_map[int(self.X_tile[0])][int(self.X_tile[1])]                                                                              ## get the heuristic value for the X_secret tile
        Y_heuristic = self.heuristic_map[int(self.Y_tile[0])][int(self.Y_tile[1])]                                                                              ## get the heuristic value for the Y_secret tile

        #print("X_heuristic ", X_heuristic)                                                                                                                      ## used for debugging
        #print("Y_heuristic ", Y_heuristic)                                                                                                                      ## used for debugging

        ## creates the initial heuritic map in reference to farther secret tile + closer secret tile heuristic + 1
        for i in range(len(self.map_data)):                                                                                                                     ## for each of the rows                                                                                                                 
            secret_heuristic.append([])                                                                                                                         ## initalize space for columns
            for j in range(len(self.map_data[0])):                                                                                                              ## for each column
                if X_heuristic < Y_heuristic:                                                                                                                   ## if the X_secret heuristic value is less than Y_secret heuristic value (if X_secret tile is closer than Y_secret tile)
                    secret_heuristic[i].append(self.manhattan_heuristic(int(self.Y_tile[0]), int(self.Y_tile[1]), self.map_data[i][j]) + X_heuristic + 1)       ## create a heuristic map from the Y_secret tile where each value is an additional X_secret heuristic + 1 away
                elif X_heuristic > Y_heuristic:                                                                                                                 ## if the Y_secret heuristic value is less than X_secret heuristic value (if Y_secret tile is closer than X_secret tile)
                    secret_heuristic[i].append(self.manhattan_heuristic(int(self.X_tile[0]), int(self.X_tile[1]), self.map_data[i][j]) + Y_heuristic + 1)       ## create a heuristic map from the X_secret tile where each value is an additional Y_secret heuristic + 1 away
                else:                                                                                                                                           ## otherwise
                    secret_heuristic[i].append(self.heuristic_map[i][j])                                                                                        ## have the heuristic value be the heuristic value from the player

        ## Keep only the smaller heuristic from each matrix of heuristics
        for i in range(len(self.map_data)):                                                                                                                     ## for each of the rows
            for j in range(len(self.map_data[0])):                                                                                                              ## for each of the columns
                if secret_heuristic[i][j] < self.heuristic_map[i][j]:                                                                                           ## determine which heuristic has the lower value
                    self.heuristic_map[i][j] = secret_heuristic[i][j]                                                                                           ## keep only the smaller value

        #print("heuristic_map ", self.heuristic_map)                                                                                                             ## used for debugging
        #print("player location, ", self.row, self.column)                                                                                                       ## used for debugging

        ## creates the initial heuritic map in reference to the goal location
        for i in range(len(self.map_data)):                                                                                                                     ## for each of the rows                                                                 
            goal_heuristic_map.append([])                                                                                                                       ## initalize space for columns
            for j in range(len(self.map_data[0])):                                                                                                              ## for each column
                goal_heuristic_map[i].append(self.manhattan_heuristic(goal[0], goal[1], self.map_data[i][j]))                                                   ## determine the manhattan heuristic in reference to the location of the player
        #print("goal heuristic_map ", goal_heuristic_map)                                                                                                        ## used for debugging

        X_goal_heuristic = goal_heuristic_map[int(self.X_tile[0])][int(self.X_tile[1])]                                                                         ## get the heuristic value for the X_secret tile
        Y_goal_heuristic = goal_heuristic_map[int(self.Y_tile[0])][int(self.Y_tile[1])]                                                                         ## get the heuristic value for the Y_secret tile

        #print("X_goal_heuristic ", X_goal_heuristic)                                                                                                            ## used for debugging
        #print("Y_goal_heuristic ", Y_goal_heuristic)                                                                                                            ## used for debugging

        ## creates the initial heuritic map in reference to farther secret tile + closer secret tile heuristic + 1
        for i in range(len(self.map_data)):                                                                                                                     ## for each of the rows                                                                                                                 
            secret_goal_heuristic.append([])                                                                                                                    ## initalize space for columns
            for j in range(len(self.map_data[0])):                                                                                                              ## for each column
                if X_goal_heuristic < Y_goal_heuristic:                                                                                                         ## if the X_goal_heuristic heuristic value is less than Y_goal_heuristic heuristic value (if X_secret tile is closer than Y_secret tile)
                    secret_goal_heuristic[i].append(self.manhattan_heuristic(int(self.Y_tile[0]), int(self.Y_tile[1]),                                          ## create a heuristic map from the Y_goal_heuristic tile where each value is an additional X_goal_heuristic + 1 away
                                                                                self.map_data[i][j]) + X_goal_heuristic + 1)   
                elif X_goal_heuristic > Y_goal_heuristic:                                                                                                       ## if the Y_goal_heuristic heuristic value is less than X_goal_heuristic heuristic value (if Y_secret tile is closer than X_secret tile)
                    secret_goal_heuristic[i].append(self.manhattan_heuristic(int(self.X_tile[0]), int(self.X_tile[1]),                                          ## create a heuristic map from the X_goal_heuristic tile where each value is an additional Y_goal_heuristic + 1 away
                                                                            self.map_data[i][j]) + Y_goal_heuristic + 1)  
                else:                                                                                                                                           ## otherwise
                    secret_goal_heuristic[i].append(goal_heuristic_map[i][j])                                                                                   ## have the heuristic value be the heuristic value from the player
        #print("secret_goal_heuristic ", secret_goal_heuristic)                                                                                                  ## used for debugging

        ## Keep only the smaller heuristic from each matrix of heuristics
        for i in range(len(self.map_data)):                                                                                                                     ## for each of the rows
            for j in range(len(self.map_data[0])):                                                                                                              ## for each of the columns
                if secret_goal_heuristic[i][j] < goal_heuristic_map[i][j]:                                                                                      ## determine which heuristic has the lower value
                    goal_heuristic_map[i][j] = secret_goal_heuristic[i][j]                                                                                      ## keep only the smaller value


        #print("goal_heuristic_map ", goal_heuristic_map)                                                                                                        ## used for debugging
        #print("heuristic_map ", self.heuristic_map)                                                                                                             ## used for debugging
        for i in range(len(self.map_data)):                                                                                                                     ## for each of the rows
            for j in range(len(self.map_data[0])):                                                                                                              ## for each of the columns
                self.heuristic_map[i][j] = self.heuristic_map[i][j] + goal_heuristic_map[i][j]                                                                  ## add the two heuristic values together
        #print("heuristic_map ", self.heuristic_map)                                                                                                             ## used for debugging 

    def cost_calulator(self, action_path):
        cal_cost = 0
        planned_r = 0
        planned_g = 0
        planned_b = 0
        for i in range(len(action_path)):                                                                                                                       ## check each item in the action path
            match action_path[i]:                                                                                                                               ## check the action item
                case "u":                                                                                                                                       ## if it was move up
                    cal_cost += 1                                                                                                                               ## add one to the cost
                case "d":                                                                                                                                       ## if it was move down
                    cal_cost += 1                                                                                                                               ## add one to the cost
                case "l":                                                                                                                                       ## if it was move left
                    cal_cost += 1                                                                                                                               ## add one to the cost
                case "r":                                                                                                                                       ## if it was move right
                    cal_cost += 1                                                                                                                               ## add one to the cost
                case "x":                                                                                                                                       ## if it was go through the x secret tunnel
                    cal_cost += 1                                                                                                                               ## add one to the cost
                case "y":                                                                                                                                       ## if it was go through the y secret tunnel
                    cal_cost += 1                                                                                                                               ## add one to the cost
                case "rt":                                                                                                                                      ## it was pick up a red token
                    cal_cost = 4 - self.Strength + cal_cost                                                                                                     ## adds cost (1 cost if Strength = 3, 2 cost is Strength = 2, 3 cost is Strength = 1)
                    planned_r += 1                                                                                                                              ## adds 1 to the planned red tokens
                case "gt":                                                                                                                                      ## if it was pick up a red token
                    cal_cost = 4 - self.Agility + cal_cost                                                                                                      ## adds cost (1 cost if Agility = 3, 2 cost is Agility = 2, 3 cost is Agility = 1)
                    planned_g += 1                                                                                                                              ## adds 1 to the planned red tokens
                case "bt":                                                                                                                                      ## if it was pick up blue token
                    planned_b += 1                                                                                                                              ## adds 1 to the planned red tokens
                    cal_cost = 4 - self.Intelligence + cal_cost                                                                                                 ## adds cost (1 cost if Intelligence = 3, 2 cost is Intelligence = 2, 3 cost is Intelligence = 1)
                case "ret":                                                                                                                                     ## if it was break the red event token
                    cal_cost += 1                                                                                                                               ## add one to the cost
                case "get":                                                                                                                                     ## if it was break the green event token
                    cal_cost += 1                                                                                                                               ## add one to the cost
                case "bet":                                                                                                                                     ## if it was break the blue event token
                    cal_cost += 1                                                                                                                               ## add one to the cost
                case "foe":                                                                                                                                     ## if it was grab the fire of eidolon
                    cal_cost += 1                                                                                                                               ## add one to the cost

        return cal_cost, planned_r, planned_g, planned_b                                                                                                        ## returns the calculated cost and the amounts of tokens planned to grab

    def auto(self):
        print('todo ', self.todo)
        print('keycount', self.keycount)
        try:
            step = self.todo[0]
            automove.automove(self, step)
        except IndexError:
            self.moving = False
            if self.todo == [] and self.keycount < 3:
                self.keycount += 1                                                                                                                                  ## passes there action
                self.actions.append("P")
            print('AUTOMOVE DONE!')            
    
    def make_token_map(self):
        settings.token_map = []                                                                                                                                 ## initalizes the token_map
        settings.red_token_locations = []            ## list of the locations of the red tokens
        settings.green_token_locations = []          ## list of the locations of the green tokens
        settings.blue_token_locations = []           ## list of the locations of the blue tokens

        ## creates the initial token map
        for i in range(len(self.map_data)):                                                                                                                 ## for each of the rows                                                                 
            settings.token_map.append([])                                                                                                                       ## initalize space for columns
            for j in range(len(self.map_data[0])):                                                                                                          ## for each column
                if tile_textures[self.map_data[i][j]].token != None:                                                                                        ## If there is a tile there
                    match tile_textures[self.map_data[i][j]].type:                                                                                          ## determine what the tile type is
                        case "Red":                                                                                                                         ## if it's listed as red
                            settings.token_map[i].append("r")                                                                                                   ## has a red token
                            settings.red_token_locations.append((i,j))
                        case "Green":                                                                                                                       ## if it's listed as green
                            settings.token_map[i].append("g")                                                                                                   ## has a green token
                            settings.green_token_locations.append((i,j))
                        case "Blue":                                                                                                                        ## if it's listed as blue
                            settings.token_map[i].append("b")                                                                                                   ## has a blue token
                            settings.blue_token_locations.append((i,j))
                        case "RedEvent":                                                                                                                    ## if it's listed as red event
                            settings.token_map[i].append("red")                                                                                                 ## has a red event token
                        case "GreenEvent":                                                                                                                  ## if it's listed as green event 
                            settings.token_map[i].append("ge")                                                                                                  ## has a green even token
                        case "BlueEvent":                                                                                                                   ## if it's listed as blue event
                            settings.token_map[i].append("be")                                                                                                  ## has a blue event token
                        case "FireofEidolon":                                                                                                               ## if it's listed as Fire of Eidolon
                            settings.token_map[i].append("foe")                                                                                                 ## has a fire of Eidolong token
                        case _:                                                                                                                             ## otherwise
                            settings.token_map[i].append("n")                                                                                                   ## has no token
                else:                                                                                                                                       ## otherwise
                    settings.token_map[i].append("n")                                                                                                           ## has no token