# Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/player.py
import pygame
import time
import settings
import numpy as np
from tilemap import *

TILE_SIZE = settings.TILE_SIZE  ## Gets the size of the tile from the settings file and sets it as a global variable

##############################################################################################################################################################################################################################
#### Things to add to player
####    - Can only go through doors if both tiles match doors (comment code and add border total)
####    - Pick up and keep track of tokens (adjust which tokens it's allowed to pick up and ad accordingly)
####    - Pick up event tokens
####    - Win Condition and display
####    - Astar with backpath (actions taken)
####    - Have the player build the map as they go
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

    def update(self):
        self.get_event()

    def get_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            #print("self.row", self.row)
            #print("self.column", self.column)
            #print(tile_textures[self.map_data[self.row][self.column]].name)
            if tile_textures[self.map_data[self.row][self.column]].up == True:
                if tile_textures[self.map_data[self.row-1][self.column]].down == True:
                    self.move(0, -TILE_SIZE)
            # check if legal move
            #door.north == true and above & dor.south == true allow up
        if keys[pygame.K_s]:
            if tile_textures[self.map_data[self.row][self.column]].down == True:
                if tile_textures[self.map_data[self.row+1][self.column]].up == True:
                    self.move(0, +TILE_SIZE)
        if keys[pygame.K_a]:
            if tile_textures[self.map_data[self.row][self.column]].left == True:
                if tile_textures[self.map_data[self.row][self.column-1]].right == True:
                    self.move(-TILE_SIZE, 0)
        if keys[pygame.K_d]:
            if tile_textures[self.map_data[self.row][self.column]].right == True:
                if tile_textures[self.map_data[self.row][self.column+1]].left == True:
                    self.move(+TILE_SIZE, 0)
        if keys[pygame.K_e]:
            print(tile_textures[self.map_data[self.row][self.column]].token)
            if tile_textures[self.map_data[self.row][self.column]].token != None:
                tile_textures[self.map_data[self.row][self.column]].token = None
                self.Green_Token = self.Green_Token + 1
                print("heres a thing")


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.row = self.row + dy//TILE_SIZE
        self.column = self.column + dx//TILE_SIZE
        time.sleep(0.5)
