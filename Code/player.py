# Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/player.py
import pygame
import time
import settings
import numpy as np
from tilemap import *

TILE_SIZE = settings.TILE_SIZE  ## Gets the size of the tile from the settings file and sets it as a global variable

##############################################################################################################################################################################################################################
#### Things to add to player
####    - Shows path taken when you win
####    - Adds a total cost
####    - Have the player build the map as they go
####    - Have it keep track of total cost of the path
####    - Use automated system such as Astar
####    - Add a 2nd player
####    - Add Spcecialisations
##############################################################################################################################################################################################################################
def create_player_texture(name):
    image = pygame.transform.scale(name,(TILE_SIZE/4,TILE_SIZE/4))                  ## scales the image to 1/4 of a tile size
    return image                                                                    ## return the token image


## Creates a player
class Player(pygame.sprite.Sprite):                                                
    def __init__(self, sprites_group, map_data):
        self.groups = sprites_group                                                 ##
        pygame.sprite.Sprite.__init__(self, self.groups)                            ##
        self.map_data = map_data
        self.image = pygame.image.load("Images/Player/GreenKnight.png")             ## sets the players image and loads the file
        self.image = create_player_texture(self.image)                              ## scales the image for use
        self.rect = self.image.get_rect()                                           ## 
        self.start_point = np.where(map_data == 1)                                  ## determines where the starting point in the map is
        self.row = int(self.start_point[0])
        self.column = int(self.start_point[1])
        self.rect.centerx = self.column*TILE_SIZE + TILE_SIZE/2                     ## places the player at the starting point's x position
        self.rect.centery = self.row*TILE_SIZE + TILE_SIZE/2                        ## places the player at the starting point's y position
        self.Green_Token = 0                                                        ## initalizes the green token count
        self.Red_Token = 0                                                          ## initalizes the red token count
        self.Blue_Token = 0                                                         ## initalizes the blue token count
        self.FireofEidolon = 0                                                      ## initalizes the grabbing of the Fire of Eidolon
        self.visited = [[self.row, self.column]]                                      ## keeps track of the locations visited (starting with the starting points)
        self.actions = ["S"]                                                        ## keeps track of actions taken (starting with S for Start)

    def update(self):
        self.get_event()

    def get_event(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if tile_textures[self.map_data[self.row][self.column]].up == True:
                if self.row-1 >= 0:                                                                                                                             ## makes sure player doesn't walk off edge
                    if tile_textures[self.map_data[self.row-1][self.column]].down == True:
                        self.actions.append("U")                                                                                                                ## remembers it moved up
                        self.move(0, -TILE_SIZE)

        if keys[pygame.K_s]:
            if tile_textures[self.map_data[self.row][self.column]].down == True:
                if self.row+1 < len(self.map_data):                                                                                                             ## makes sure player doesn't walk off edge
                    if tile_textures[self.map_data[self.row+1][self.column]].up == True:
                        self.actions.append("D")                                                                                                                ## remembers it moved down
                        self.move(0, +TILE_SIZE)

        if keys[pygame.K_a]:
            if tile_textures[self.map_data[self.row][self.column]].left == True:
                if self.column-1 >= 0:                                                                                                                          ## makes sure player doesn't walk off edge
                    if tile_textures[self.map_data[self.row][self.column-1]].right == True:
                        self.actions.append("L")                                                                                                                ## remembers it moved left
                        self.move(-TILE_SIZE, 0)

        if keys[pygame.K_d]:
            if tile_textures[self.map_data[self.row][self.column]].right == True:
                if self.column+1 < len(self.map_data[0]):                                                                                                      ## makes sure player doesn't walk off edge
                    if tile_textures[self.map_data[self.row][self.column+1]].left == True:
                        self.actions.append("R")                                                                                                                ## remembers it moved right
                        self.move(+TILE_SIZE, 0)
        if keys[pygame.K_p]:
            print("map ", self.map_data)
            print("player location, ", self.row, self.column)
            print("Doors, ", tile_textures[self.map_data[self.row][self.column]].left)
 
        ## Grabs tokens
        if keys[pygame.K_e]:
            if tile_textures[self.map_data[self.row][self.column]].token != None:
                match tile_textures[self.map_data[self.row][self.column]].type:
                    case "Red":                                                                                                                                 ## if it's listed as red
                        self.Red_Token = self.Red_Token + 1                                                                                                     ## increase the Red_Token by 1
                        tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                    case "Green":                                                                                                                               ## if it's listed as green
                        self.Green_Token = self.Green_Token + 1                                                                                                 ## increase the Green_Token by 1
                        tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                    case "Blue":                                                                                                                                ## if it's listed as blue
                        self.Blue_Token = self.Blue_Token + 1                                                                                                   ## increase the Green_Token by 1
                        tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                    case "RedEvent":                                                                                                                            ## if it's listed as red event
                        if self.Red_Token >= 6:                                                                                                                 ## do you have enough tokens to break the red event
                            settings.Red_Event_Broken = True                                                                                                    ## breaks the red event
                            tile_textures[self.map_data[self.row][self.column]].type = "Broken_RedEvent"                                                        ## displays the broken red event token
                            tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                    case "GreenEvent":                                                                                                                          ## if it's listed as green event 
                        if self.Green_Token >= 6:                                                                                                               ## do you have enough tokens to break the green event
                            settings.Green_Event_Broken = True                                                                                                  ## breaks the green event
                            tile_textures[self.map_data[self.row][self.column]].type = "Broken_GreenEvent"                                                      ## displays the broken green event token
                            tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                    case "BlueEvent":                                                                                                                           ## if it's listed as blue event
                        if self.Blue_Token >= 6:                                                                                                                ## do you have enough tokens to break the blue event
                            settings.Blue_Event_Broken = True                                                                                                   ## breaks the blue event
                            tile_textures[self.map_data[self.row][self.column]].type = "Broken_BlueEvent"                                                       ## displays the broken blue event token
                            tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                    case "FireofEidolon":                                                                                                                       ## if it's listed as Fire of Eidolon
                        if settings.Red_Event_Broken == True and settings.Green_Event_Broken == True and settings.Blue_Event_Broken == True:                    ## all other events broken?
                            settings.FireofEidolon_Grabbed = True                                                                                               ## marks that the Fire of Eidolon has been grabbed
                            self.FireofEidolon = 1                                                                                                              ## indicates that the player has the Fire of Eidolon
                            tile_textures[self.map_data[self.row][self.column]].token = None                                                                    ## Removes the token
                self.actions.append("T")                                                                                                                    ## remembers it grabbed a token (or at least tired)


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.row = self.row + dy//TILE_SIZE
        self.column = self.column + dx//TILE_SIZE
        self.visited.append([self.row, self.column])
        if tile_textures[self.map_data[self.row][self.column]].name == "EndTile" and self.FireofEidolon == 1:
            print("You Win!")
            print(self.visited)
            print(self.actions)
        time.sleep(0.5)
