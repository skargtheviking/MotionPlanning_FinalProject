# Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/player.py
import pygame
import time
import settings
import numpy as np
from tilemap import *
import matplotlib.pyplot as plotter
from math import hypot, sqrt
#from graph_search import astar

TILE_SIZE = settings.TILE_SIZE  ## Gets the size of the tile from the settings file and sets it as a global variable

##############################################################################################################################################################################################################################
#### Things to add to player
####    - Have the player build the map as they go
####    - Use automated system such as Astar
####    - Add a 2nd player
##############################################################################################################################################################################################################################
def create_player_texture(name):
    image = pygame.transform.scale(name,(TILE_SIZE/4,TILE_SIZE/4))                                                                                              ## scales the image to 1/4 of a tile size
    return image                                                                                                                                                ## return the token image


## Creates a player
class Player(pygame.sprite.Sprite):                                                
    def __init__(self, sprites_group, map_data, living = False):
        self.groups = sprites_group                                                                                                                             ##
        pygame.sprite.Sprite.__init__(self, self.groups)                                                                                                        ##
        self.map_data = map_data                                                                                                                                ## stores the map for the player
        self.image = pygame.image.load("Images/Player/GreenKnight.png")                                                                                         ## sets the players image and loads the file
        self.image = create_player_texture(self.image)                                                                                                          ## scales the image for use
        self.rect = self.image.get_rect()                                                                                                                       ## get the rectangle angle fo the surface
        self.Strength = 3                                                                                                                                       ## determines the players strength 
        self.Intelligence = 3                                                                                                                                   ## determines the players intelligence
        self.Agility = 3                                                                                                                                        ## determines the players Agility
        self.start_point = np.where(map_data == 1)                                                                                                              ## determines where the starting point is on the map
        self.end = np.where(map_data == 6)                                                                                                                      ## determines where the end tile is
        self.goal = self.end                                                                                                                                    ## determien a goal tile
        self.X_tile = np.where(map_data == 7)                                                                                                                   ## determines where the secret X tile is on the map
        self.Y_tile = np.where(map_data == 8)                                                                                                                   ## determines where the secret Y tile is on the map
        self.row = int(self.start_point[0])                                                                                                                     ## This is the row the player is at
        self.column = int(self.start_point[1])                                                                                                                  ## This is the column the player is at
        self.rect.centerx = self.column*TILE_SIZE + TILE_SIZE/2                                                                                                 ## places the player at the starting point's x position
        self.rect.centery = self.row*TILE_SIZE + TILE_SIZE/2                                                                                                    ## places the player at the starting point's y position
        self.Green_Token = 0                                                                                                                                    ## initalizes the green token count
        self.Red_Token = 0                                                                                                                                      ## initalizes the red token count
        self.Blue_Token = 0                                                                                                                                     ## initalizes the blue token count
        self.FireofEidolon = 0                                                                                                                                  ## initalizes the grabbing of the Fire of Eidolon
        self.visited = [[self.row, self.column]]                                                                                                                ## keeps track of the locations visited (starting with the starting points)
        self.actions = ["S"]                                                                                                                                    ## keeps track of actions taken (starting with S for Start)
        self.totalcost = 0                                                                                                                                      ## keeps track of the total cost

    def update(self):
        self.get_event()

    def get_event(self):
        keys = pygame.key.get_pressed()

        ## Moving Up
        if keys[pygame.K_w]:                                                                                                                                    ## when the "W" button is pressed
            if 'u' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                if self.row-1 >= 0:                                                                                                                             ## makes sure player doesn't walk off edge
                    if 'd' in tile_textures[self.map_data[self.row-1][self.column]].quickinfo:
                        self.actions.append("U")                                                                                                                ## remembers it moved up
                        self.move(0, -TILE_SIZE)

        ## Moving Down
        if keys[pygame.K_s]:
            if 'd' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                if self.row+1 < len(self.map_data):                                                                                                             ## makes sure player doesn't walk off edge
                    if 'u' in tile_textures[self.map_data[self.row+1][self.column]].quickinfo:
                        self.actions.append("D")                                                                                                                ## remembers it moved down
                        self.move(0, +TILE_SIZE)
        ## Moving Left
        if keys[pygame.K_a]:
            if 'l' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                if self.column-1 >= 0:                                                                                                                          ## makes sure player doesn't walk off edge
                    if 'r' in tile_textures[self.map_data[self.row][self.column-1]].quickinfo:
                        self.actions.append("L")                                                                                                                ## remembers it moved left
                        self.move(-TILE_SIZE, 0)
        ## Moving Right
        if keys[pygame.K_d]:
            if 'r' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                if self.column+1 < len(self.map_data[0]):                                                                                                      ## makes sure player doesn't walk off edge
                    if 'l' in tile_textures[self.map_data[self.row][self.column+1]].quickinfo:
                        self.actions.append("R")                                                                                                                ## remembers it moved right
                        self.move(+TILE_SIZE, 0)

        ## Calculate Heristic of map 
        if keys[pygame.K_h]:
            self.huristic_map = []                                                                                                                              ## initalizes the huristic_map
            for i in range(len(self.map_data)):                                                                                                                 ## for each row
                self.huristic_map.append([])                                                                                                                    ## make a list of columns
                for j in range(len(self.map_data[0])):                                                                                                          ## for each of the columns
                    self.huristic_map[i].append(self.euclidean_heuristic(self.map_data[i][j]))                                                                  ## determine the huristic cost to for each point
            #print("map ", self.map_data)                                                                                                                        ## used for debugging
            #print("huristic ", self.huristic_map)                                                                                                               ## used for debugging
            #print("player location, ", self.row, self.column)                                                                                                   ## used for debugging
            time.sleep(0.5)                                                                                                                                     ## gives the computer a time before reading the next keystroke

       ## set goal
        if keys[pygame.K_g]:
            self.goal = [self.row,self.column]

        ## A-Star to somewhere
        if keys[pygame.K_p]:
            #astar(self.map_data,[self.row, self.column],tiles, )
            self.huristic_map = []                                                                                                                ## initalizes the huristic_map
            for i in range(len(self.map_data)):
                self.huristic_map.append([])
                for j in range(len(self.map_data[0])):
                    self.huristic_map[i].append(self.euclidean_heuristic(self.map_data[i][j]))
            print("map ", self.map_data)
            print("huristic ", self.huristic_map)
            print("player location, ", self.row, self.column)
            time.sleep(0.5)      

        ## Grabs tokens
        if keys[pygame.K_e]:                                                                                                                                    ## when the "E" button is pressed
            if tile_textures[self.map_data[self.row][self.column]].token != None:                                                                               ## If there is a tile there
                match tile_textures[self.map_data[self.row][self.column]].type:                                                                                 ## determine what the tile type is
                    case "Red":                                                                                                                                 ## if it's listed as red
                        self.totalcost = 4 - self.Strength + self.totalcost                                                                                     ## adds cost (1 cost if Strength = 3, 2 cost is Strength = 2, 3 cost is Strength = 1)
                        self.Red_Token = self.Red_Token + 1                                                                                                     ## increase the Red_Token by 1
                        tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                        tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("rt")                                                              ## Removes the token from quick info
                    case "Green":                                                                                                                               ## if it's listed as green
                        self.totalcost = 4 - self.Agility + self.totalcost                                                                                      ## adds cost (1 cost if Agility = 3, 2 cost is Agility = 2, 3 cost is Agility = 1)
                        self.Green_Token = self.Green_Token + 1                                                                                                 ## increase the Green_Token by 1
                        tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                        tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("gt")                                                              ## Removes the token from quick info
                    case "Blue":                                                                                                                                ## if it's listed as blue
                        self.totalcost = 4 - self.Intelligence + self.totalcost                                                                                 ## adds cost (1 cost if Intelligence = 3, 2 cost is Intelligence = 2, 3 cost is Intelligence = 1)
                        self.Blue_Token = self.Blue_Token + 1                                                                                                   ## increase the Blue_Token by 1
                        tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                        tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("bt")                                                              ## Removes the token from quick info
                    case "RedEvent":                                                                                                                            ## if it's listed as red event
                        if self.Red_Token >= 6:                                                                                                                 ## do you have enough tokens to break the red event
                            self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to break event
                            settings.Red_Event_Broken = True                                                                                                    ## breaks the red event
                            tile_textures[self.map_data[self.row][self.column]].type = "Broken_RedEvent"                                                        ## displays the broken red event token
                            tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                            tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("ret")                                                         ## Removes the token from quick info
                    case "GreenEvent":                                                                                                                          ## if it's listed as green event 
                        if self.Green_Token >= 6:                                                                                                               ## do you have enough tokens to break the green event
                            self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to break event
                            settings.Green_Event_Broken = True                                                                                                  ## breaks the green event
                            tile_textures[self.map_data[self.row][self.column]].type = "Broken_GreenEvent"                                                      ## displays the broken green event token
                            tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                            tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("get")                                                         ## Removes the token from quick info
                    case "BlueEvent":                                                                                                                           ## if it's listed as blue event
                        if self.Blue_Token >= 6:                                                                                                                ## do you have enough tokens to break the blue event
                            self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to break event
                            settings.Blue_Event_Broken = True                                                                                                   ## breaks the blue event
                            tile_textures[self.map_data[self.row][self.column]].type = "Broken_BlueEvent"                                                       ## displays the broken blue event token
                            tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                            tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("bet")                                                         ## Removes the token from quick info
                    case "FireofEidolon":                                                                                                                       ## if it's listed as Fire of Eidolon
                        if settings.Red_Event_Broken == True and settings.Green_Event_Broken == True and settings.Blue_Event_Broken == True:                    ## all other events broken?
                            self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to grab Fire of Eidolon
                            settings.FireofEidolon_Grabbed = True                                                                                               ## marks that the Fire of Eidolon has been grabbed
                            self.FireofEidolon = 1                                                                                                              ## indicates that the player has the Fire of Eidolon
                            tile_textures[self.map_data[self.row][self.column]].token = None                                                                    ## Removes the token
                            tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("foe")                                                         ## Removes the token from quick info
                print(self.totalcost)                                                                                                                           ## used for debugging 
                self.actions.append("T")                                                                                                                        ## remembers it grabbed a token (or at least tired)

        ## Use Tunnel
        if keys[pygame.K_q]:                                                                                                                                    ## when the "Q" button is pressed
            if tile_textures[self.map_data[self.row][self.column]].name == "SecretX":                                                                           ## if on secret X tile              
                self.row = int(self.Y_tile[0])                                                                                                                  ## This is the row the player is at
                self.column = int(self.Y_tile[1])                                                                                                               ## This is the column the player is at
                self.rect.centerx = self.column*TILE_SIZE + TILE_SIZE/2                                                                                         ## places the player at the Secret Y's x position
                self.rect.centery = self.row*TILE_SIZE + TILE_SIZE/2                                                                                            ## places the player at the Secret Y's y position
                self.actions.append("X")                                                                                                                        ## Used the secret X tunnel
                self.move(0, 0)                                                                                                                                 ## records where the player went
            elif tile_textures[self.map_data[self.row][self.column]].name == "SecretY":                                                                         ## if on a secret Y tile                  
                self.row = int(self.X_tile[0])                                                                                                                  ## This is the row the player is at
                self.column = int(self.X_tile[1])                                                                                                               ## This is the column the player is at
                self.rect.centerx = self.column*TILE_SIZE + TILE_SIZE/2                                                                                         ## places the player at the Secret Y's x position
                self.rect.centery = self.row*TILE_SIZE + TILE_SIZE/2                                                                                            ## places the player at the Secret Y's y position
                self.actions.append("Y")                                                                                                                        ## Used the secret Y tunnel
                self.move(0, 0)                                                                                                                                 ## records where the player went
            print(self.totalcost)                                                                                                                               ## used for debugging 
            time.sleep(0.5)                                                                                                                                     ## gives the computer a time before reading the next keystroke

    ## moves the player on the screen and where the player is on the map
    def move(self, dx, dy):
        self.totalcost = self.totalcost + 1                                                                                                                     ## adds 1 to the total cost
        print(self.totalcost)                                                                                                                                   ## used for debugging
        self.rect.x += dx                                                                                                                                       ## lets the compter know where to move the player in the x direction
        self.rect.y += dy                                                                                                                                       ## lets the compter know where to move the player in the y direction
        self.row = self.row + dy//TILE_SIZE                                                                                                                     ## sets the new row
        self.column = self.column + dx//TILE_SIZE                                                                                                               ## sets the new column
        self.visited.append([self.row, self.column])                                                                                                            ## saves the tile visited
        if tile_textures[self.map_data[self.row][self.column]].name == "EndTile" and self.FireofEidolon == 1:                                                   ## if the player is on the End Tile and has the Fire of Eidolon
            settings.Win = True
            print("You Win!")                                                                                                                                   ## let the player know they won
            print("Vistied ", self.visited)                                                                                                                     ## displays the visited tiles in order of vist
            print("Actions ", self.actions)                                                                                                                     ## displays the actions in order of taken
            print("Total Cost ", self.totalcost)                                                                                                                ## displays the total costs to win
            settings.Player_1 = self                                                                                                                            ## sets player 1 as itself
        time.sleep(0.5)                                                                                                                                         ## gives the computer a time before reading the next keystroke

    ## Calculating the euclidean huristic value between two points
    def euclidean_heuristic(self, tile_num):
        #print("tile_num ", tile_num)                                                                                                                            ## used for debugging
        if tile_num != 0:                                                                                                                                       ## skip if the goal is 0
            point = [0,0]                                                                                                                                       ## initalizes the point
            tile = np.where(self.map_data == tile_num)                                                                                                          ## to search by tile type
            #print("tile ", tile)                                                                                                                                ## used for debugging
            point[0] = int(tile[0][-1])                                                                                                                         ## sets the row of the point
            point[1] = int(tile[1][-1])                                                                                                                         ## sets the column of the point
            #print("Point ", point)                                                                                                                              ## used for debugging
            dis = sqrt((self.row-point[0])**2 + (self.column-point[1])**2)                                                                                      ## cacluate the euclidean huristic between the player point and the tile number goal
        else:                                                                                                                                                   ## if tile looking for is 0
            dis = -1                                                                                                                                            ## just set the distance to -1 (impossible)
        return dis                                                                                                                                              ## return the distance calculated


